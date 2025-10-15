import logging
import requests
from django.contrib.auth.models import AnonymousUser
from cryptography.hazmat.primitives import serialization
from rest_framework.permissions import BasePermission
from functools import lru_cache
from rest_framework import authentication, exceptions
import jwt
from django.conf import settings

logger = logging.getLogger(__name__)

# =============================================
# 1. CLASSES UTILITAIRES (inchangées)
# =============================================
class KeycloakUser:
    """Utilisateur fantôme avec rôles Keycloak."""
    def __init__(self, username, email, roles):
        self.username = username
        self.email = email
        self.roles = roles
        self.is_authenticated = True
        self.is_active = True

    def __str__(self):
        return self.username

class KeycloakAnonymousUser(AnonymousUser):
    """Utilisateur anonyme avec attribut `roles`."""
    @property
    def roles(self):
        return []

# =============================================
# 2. FONCTIONS DE VALIDATION ET RÉCUPÉRATION CLÉ
# =============================================
def validate_pem_public_key(key: str) -> bool:
    """Valide que la clé PEM est valide (utilisé pour le fallback)."""
    try:
        serialization.load_pem_public_key(key.encode())
        return True
    except Exception as e:
        logger.error(f"Clé PEM invalide: {e}")
        return False

@lru_cache(maxsize=1)  # Cache pour éviter des appels répétés à Keycloak
def fetch_jwks_public_key() -> str:
    """
    Récupère la clé publique depuis Keycloak via le endpoint JWKS.
    Returns:
        str: Clé publique au format PEM (compatible avec PyJWT).
    Raises:
        ValueError: Si la récupération échoue (sauf en mode DEBUG où un fallback est utilisé).
    """
    jwks_url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"

    try:
        # 1. Récupère les clés JWKS depuis Keycloak
        response = requests.get(jwks_url, timeout=5)
        response.raise_for_status()  # Lève une erreur si HTTP 4xx/5xx
        jwks = response.json()

        # 2. Filtre pour ne garder que les clés RS256 (standard pour Keycloak)
        keys = [k for k in jwks["keys"] if k.get("alg") == "RS256"]
        if not keys:
            raise ValueError("Aucune clé RS256 trouvée dans le JWKS.")

        # 3. Convertit la première clé JWK en format PEM (nécessaire pour PyJWT)
        key = keys[0]
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
        pem_key = public_key.public_numbers().public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem_key.decode('utf-8')  # PyJWT attend une string, pas des bytes

    except requests.exceptions.RequestException as e:
        logger.error(f"Échec de la connexion à Keycloak (JWKS): {e}")
        if settings.DEBUG:
            # ✅ FALLBACK EN DÉVELOPPEMENT UNIQUEMENT: Utilise une clé PEM statique si Keycloak est inaccessible
            fallback_key = getattr(settings, "KEYCLOAK_PUBLIC_KEY_FALLBACK", None)
            if fallback_key and validate_pem_public_key(fallback_key.replace('\\n', '\n')):
                logger.warning("Utilisation de la clé de fallback (mode DEBUG uniquement !)")
                return fallback_key.replace('\\n', '\n')
        raise ValueError("Impossible de récupérer la clé publique depuis Keycloak.")

    except Exception as e:
        logger.error(f"Erreur inattendue lors de la récupération du JWKS: {e}")
        raise ValueError("Configuration Keycloak invalide.")

# =============================================
# 3. CLASSE D'AUTHENTIFICATION
# =============================================
class KeycloakAuthentication(authentication.BaseAuthentication):
    def __init__(self):
        super().__init__()
        # Validation au démarrage: Vérifie que Keycloak est accessible et que la clé est valide
        try:
            public_key = fetch_jwks_public_key()  # ✅ Utilise la clé dynamique
            if not validate_pem_public_key(public_key):
                raise ValueError("La clé publique récupérée depuis Keycloak est invalide.")
        except Exception as e:
            logger.critical(f"Échec de l'initialisation de KeycloakAuth: {e}")
            raise  # Propage l'erreur pour bloquer le démarrage si Keycloak est indisponible

    @staticmethod
    @lru_cache(maxsize=1)
    def _get_keycloak_config():
        """Retourne la configuration Keycloak (sans la clé publique, désormais dynamique)."""
        config = {
            'SERVER_URL': settings.KEYCLOAK_SERVER_URL,
            'REALM': settings.KEYCLOAK_REALM,
            'CLIENT_ID': settings.KEYCLOAK_CLIENT_ID,
            'ALGORITHM': 'RS256',
        }
        if not all(config.values()):
            raise ValueError("Configuration Keycloak incomplète dans les settings.")
        return config

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return (KeycloakAnonymousUser(), None)  # Utilisateur anonyme si pas de token

        try:
            # 1. Vérifie le format du header
            if not auth_header.startswith('Bearer '):
                raise exceptions.AuthenticationFailed("Le header Authorization doit commencer par 'Bearer '")

            token = auth_header.split(' ')[1]
            config = self._get_keycloak_config()

            # 2. Récupère la clé publique (via cache)
            public_key = fetch_jwks_public_key()

            # 3. Décode et valide le token JWT
            payload = jwt.decode(
                token,
                public_key,  # ✅ Utilise la clé dynamique
                algorithms=[config['ALGORITHM']],
                audience=config['CLIENT_ID'],  # Vérifie que le token est destiné à ce client
                issuer=f"{config['SERVER_URL']}/realms/{config['REALM']}",  # Vérifie l'émetteur
            )

            # 4. Extrait les rôles (resource_access + realm_access)
            client_roles = payload.get('resource_access', {}).get(config['CLIENT_ID'], {}).get('roles', [])
            realm_roles = payload.get('realm_access', {}).get('roles', [])
            roles = list(set(client_roles + realm_roles))  # Évite les doublons

            # 5. Extrait les infos utilisateur
            email = payload.get('email')
            username = payload.get('preferred_username', email.split('@')[0]) if email else None

            if not email or not username:
                raise exceptions.AuthenticationFailed("Email ou username manquant dans le token.")

            logger.info(f"Utilisateur {username} authentifié avec rôles: {roles}")
            return (KeycloakUser(username=username, email=email, roles=roles), token)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expiré.", code="token_expired")
        except jwt.InvalidTokenError as e:
            logger.error(f"Token JWT invalide: {str(e)}")
            raise exceptions.AuthenticationFailed("Token invalide.", code="token_invalid")
        except Exception as e:
            logger.error(f"Erreur d'authentification: {str(e)}", exc_info=True)
            return (KeycloakAnonymousUser(), None)  # Retourne un utilisateur anonyme en cas d'erreur

# =============================================
# 4. PERMISSIONS (inchangées)
# =============================================
class IsKeycloakAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and 'admin' in request.user.roles

class IsKeycloakUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and any(role in request.user.roles for role in ['user', 'admin'])
