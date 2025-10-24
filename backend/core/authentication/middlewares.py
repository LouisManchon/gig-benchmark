from django.contrib.auth.models import AnonymousUser
from core.authentication.keycloak_auth import KeycloakAnonymousUser

class AnonymousUserMiddleware:
    """Middleware qui remplace AnonymousUser par KeycloakAnonymousUser.
    Cela évite les AttributeError quand on essaie d'accéder à request.user.roles.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérifie si l'utilisateur est anonyme (non authentifié)
        if not hasattr(request, 'user') or isinstance(request.user, AnonymousUser):
            request.user = KeycloakAnonymousUser()  # ✅ Remplace par notre classe custom

        return self.get_response(request)
