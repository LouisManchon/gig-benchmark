import os
import logging
from rest_framework import authentication, exceptions
from django.contrib.auth.models import User
import jwt
from jwt.algorithms import RSAAlgorithm

logger = logging.getLogger(__name__)

class KeycloakAuthentication(authentication.BaseAuthentication):
    """
    Authentification Keycloak avec PyJWT et validation RS256.
    Compatible avec :
    - Ta config .env actuelle
    - Ton settings.py (Django 4.x + DRF)
    - Les rôles Keycloak dans `realm_access.roles`
    """

    @staticmethod
    def _get_keycloak_config():
        """Charge la configuration depuis settings.py (déjà défini dans ton code)"""
        from django.conf import settings
        return {
            'SERVER_URL': settings.KEYCLOAK_SERVER_URL,
            'REALM': settings.KEYCLOAK_REALM,
            'CLIENT_ID': settings.KEYCLOAK_CLIENT_ID,
            'PUBLIC_KEY': settings.KEYCLOAK_CLIENT_PUBLIC_KEY.replace('\\n', '\n'),
            'ALGORITHM': settings.SIMPLE_JWT['ALGORITHM'],  # RS256 (déjà dans ton .env)
        }

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            # 1. Extraction du token
            if not auth_header.startswith('Bearer '):
                raise exceptions.AuthenticationFailed("Authorization header must start with 'Bearer'")

            token = auth_header.split(' ')[1]
            config = self._get_keycloak_config()

            # 2. Validation du token avec la clé publique
            payload = jwt.decode(
                token,
                config['PUBLIC_KEY'],
                algorithms=[config['ALGORITHM']],
                audience=config['CLIENT_ID'],
                issuer=f"{config['SERVER_URL']}/realms/{config['REALM']}",
            )

            # 3. Extraction des rôles et email
            roles = payload.get('realm_access', {}).get('roles', [])
            email = payload.get('email')
            if not email:
                raise exceptions.AuthenticationFailed("No email in token")

            # 4. Création/Gestion de l'utilisateur Django (optionnel)
            user, _ = User.objects.get_or_create(
                username=payload.get('preferred_username', email.split('@')[0]),
                defaults={'email': email, 'is_active': True}
            )

            # 5. Attache les rôles à la requête pour les permissions
            request.keycloak_roles = roles
            return (user, token)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError as e:
            logger.error(f"JWT Validation Error: {str(e)}")
            raise exceptions.AuthenticationFailed("Invalid token")
        except Exception as e:
            logger.error(f"Authentication Error: {str(e)}")
            raise exceptions.AuthenticationFailed("Authentication failed")

    # === Méthodes utilitaires pour les permissions ===
    @staticmethod
    def has_role(request, role_name):
        """Vérifie si l'utilisateur a un rôle spécifique."""
        return hasattr(request, 'keycloak_roles') and role_name in request.keycloak_roles

    @staticmethod
    def user_is_admin(request):
        """Vérifie si l'utilisateur est admin."""
        return KeycloakAuthentication.has_role(request, 'admin')

    @staticmethod
    def user_is_analyst(request):
        """Vérifie si l'utilisateur est analyst."""
        return KeycloakAuthentication.has_role(request, 'analyst')
