import os
import logging
from rest_framework.permissions import BasePermission
from functools import lru_cache
from rest_framework import authentication, exceptions
import jwt
from django.conf import settings

logger = logging.getLogger(__name__)

class KeycloakUser:
    """
    Utilisateur "fantôme" qui n'utilise PAS la base de données Django.
    Stocke uniquement les infos nécessaires depuis le token Keycloak.
    """
    def __init__(self, username, email, roles):
        self.username = username      # Nom d'utilisateur (ex: "john_doe")
        self.email = email            # Email (ex: "john@example.com")
        self.roles = roles            # Rôles Keycloak (ex: ["admin", "user"])
        self.is_authenticated = True  # Obligatoire pour Django
        self.is_active = True         # Indique que le compte est actif

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<KeycloakUser: {self.username} (roles: {self.roles})>"

def get_anonymous_user():
    """Retourne un utilisateur non authentifié (remplace AnonymousUser).
    """
    user = KeycloakUser(
    username="anonymous",
    email=None,
    roles=[],
    )
    user.is_authenticated = False  # ✅ Critique pour Django
    user.is_active = False

    return user

class KeycloakAuthentication(authentication.BaseAuthentication):
    """
    Authentification Keycloak avec PyJWT et validation RS256.
    - Valide le token via la clé publique Keycloak
    - Extrait les rôles depuis `resource_access.gig-api.roles`
    - Crée un utilisateur fantôme (sans base de données)
    - Attache les rôles à la requête pour les permissions
    """

    @staticmethod
    @lru_cache(maxsize=1)  # ← Cache la config pour éviter de recharger à chaque requête
    def _get_keycloak_config():
        """Charge la configuration depuis settings.py"""
        return {
            'SERVER_URL': settings.KEYCLOAK_SERVER_URL,  # Ex: "http://localhost:8080"
            'REALM': settings.KEYCLOAK_REALM,            # Ex: "GigBenchmarkRealm"
            'CLIENT_ID': settings.KEYCLOAK_CLIENT_ID,    # Ex: "gig-api"
            'PUBLIC_KEY': settings.KEYCLOAK_PUBLIC_KEY.replace('\\n', '\n'),  # Clé publique formatée
            'ALGORITHM': 'RS256',  # Algorithme de signature (doit matcher Keycloak)
        }

    def authenticate(self, request):
        """
        Méthode principale d'authentification.
        1. Extrait le token du header Authorization
        2. Valide le token avec la clé publique Keycloak
        3. Crée un utilisateur fantôme avec les rôles
        4. Retourne (user, token) pour les vues DRF
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None  # Pas de header = pas d'authentification (401 sera renvoyé par DRF)

        try:
            # 1. Vérification du format du header
            if not auth_header.startswith('Bearer '):
                raise exceptions.AuthenticationFailed(
                    "Authorization header must start with 'Bearer '"
                )

            token = auth_header.split(' ')[1]  # Extrait "xxxx.yyyy.zzzz"
            config = self._get_keycloak_config()

            # 2. Décodage et validation du token JWT
            payload = jwt.decode(
                token,
                config['PUBLIC_KEY'],
                algorithms=[config['ALGORITHM']],
                audience=config['CLIENT_ID'],  # Vérifie que le token est pour notre client
                issuer=f"{config['SERVER_URL']}/realms/{config['REALM']}",  # Vérifie l'émetteur
            )

            # 3. Extraction des données utilisateur
            resource_roles = payload.get('resource_access', {}).get('gig-api', {}).get('roles', [])
            realm_roles = payload.get('realm_access', {}).get('roles', [])
            roles = list(set(resource_roles + realm_roles))  # Fusionne et supprime les doublons

            email = payload.get('email')
            username = payload.get('preferred_username', email.split('@')[0])  # fallback sur email

            if not email:
                raise exceptions.AuthenticationFailed("No email found in token payload")

            logger.info(f"Authenticating user {username} with roles: {roles}")

            # 4. Création de l'utilisateur fantôme (sans base de données)
            user = KeycloakUser(
                username=username,
                email=email,
                roles=roles
            )

            return (user, token)  # DRF utilisera cet utilisateur pour les permissions

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired - please login again")
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid JWT token: {str(e)}")
            raise exceptions.AuthenticationFailed("Invalid token")
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}", exc_info=True)
            raise exceptions.AuthenticationFailed("Authentication failed")

class IsKeycloakAdmin(BasePermission):
    def has_permission(self, request, view):
        # Vérifie d'abord que l'utilisateur est authentifié
        if not request.user.is_authenticated:
            return False
        return 'admin' in request.user.roles


class IsKeycloakUser(BasePermission):
    def has_permission(self, request, view):
        # Autorise si l'utilisateur a au moins un des rôles ['user', 'admin']
        return any(role in request.user.roles for role in ['user', 'admin'])
