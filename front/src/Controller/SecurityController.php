<?php
namespace App\Controller;

use KnpU\OAuth2ClientBundle\Client\ClientRegistry;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Session\SessionInterface;

class SecurityController extends AbstractController
{
    #[Route('/login', name: 'login')]
    public function login(ClientRegistry $clientRegistry)
    {
        // Redirection vers Keycloak
        return $clientRegistry->getClient('keycloak')->redirect();
    }

    #[Route('/connect/keycloak/check', name: 'connect_keycloak_check')]
    public function connectCheck(ClientRegistry $clientRegistry, SessionInterface $session)
    {
        $client = $clientRegistry->getClient('keycloak');
        $accessToken = $client->getAccessToken();
        $user = $client->fetchUserFromToken($accessToken);

        // Stocker le token et les infos utilisateur en session
        $session->set('access_token', $accessToken->getToken());
        $session->set('user', [
            'username' => $user->getNickname() ?? $user->getId(),
            'email' => $user->getEmail(),
        ]);

        // Redirection vers la page d’accueil
        return $this->redirectToRoute('home');
    }

    #[Route('/logout', name: 'logout')]
    public function logout()
    {
        $keycloakLogoutUrl = 'http://localhost:8080/realms/GigBenchmarkRealm/protocol/openid-connect/logout?redirect_uri=http://localhost:8001';
        return new RedirectResponse($keycloakLogoutUrl);
    }
}
