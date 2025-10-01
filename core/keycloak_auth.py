# core/keycloak_auth.py
from rest_framework import authentication, exceptions
from keycloak import KeycloakOpenID
import os

# Connexion au serveur Keycloak
keycloak_openid = KeycloakOpenID(
    server_url=os.getenv("KEYCLOAK_SERVER_URL"),
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    realm_name=os.getenv("KEYCLOAK_REALM"),
    client_secret_key=os.getenv("KEYCLOAK_CLIENT_SECRET_KEY", None)
)

class KeycloakAuthentication(authentication.BaseAuthentication):
    """
    Authentification DRF utilisant un token JWT Keycloak.
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # DRF continuera à tester les autres classes d'auth

        token = auth_header.split(' ')[1]
        try:
            # Vérifie le token auprès de Keycloak
            user_info = keycloak_openid.userinfo(token)
        except Exception:
            raise exceptions.AuthenticationFailed('Invalid Keycloak token')

        # Ici on retourne un "utilisateur" factice ou un objet Django User
        return (user_info, None)
