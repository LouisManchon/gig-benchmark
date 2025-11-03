<?php

namespace App\Controller;

use App\Service\AuthService;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse; // ✅ AJOUT
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Session\SessionInterface;
use Symfony\Component\Routing\Annotation\Route;

class SecurityController extends AbstractController
{
    private AuthService $authService;

    public function __construct(AuthService $authService)
    {
        $this->authService = $authService;
    }

    #[Route('/login', name: 'app_login')]
    public function login(Request $request, SessionInterface $session): Response
    {
        // Si déjà connecté, redirige vers /odds
        if ($session->has('jwt_token')) {
            return $this->redirectToRoute('odds_list');
        }

        if ($request->isMethod('POST')) {
            $username = $request->request->get('username');
            $password = $request->request->get('password');

            $result = $this->authService->login($username, $password);

            if (!empty($result['success'])) {
                // ✅ Stocker les tokens côté serveur (session)
                $session->set('jwt_token', $result['access'] ?? null);
                $session->set('jwt_refresh', $result['refresh'] ?? null);

                // Optionnel: si ton API renvoie un user, tu peux le stocker aussi
                if (!empty($result['user'])) {
                    $session->set('user', $result['user']);
                }

                $this->addFlash('success', 'Login successful!');
                return $this->redirectToRoute('odds_list');
            }

            $this->addFlash('error', $result['error'] ?? 'Invalid credentials');
        }

        return $this->render('security/login.html.twig');
    }

    #[Route('/register', name: 'app_register')]
    public function register(Request $request): Response
    {
        if ($request->isMethod('POST')) {
            $userData = [
                'username' => $request->request->get('username'),
                'email' => $request->request->get('email'),
                'password' => $request->request->get('password'),
                'password2' => $request->request->get('password2'),
            ];

            $result = $this->authService->register($userData);

            if (!empty($result['success'])) {
                $this->addFlash('success', 'Registration successful! You can now login.');
                return $this->redirectToRoute('app_login');
            }

            $errors = $result['data'] ?? [];
            foreach ($errors as $field => $messages) {
                if (is_array($messages)) {
                    foreach ($messages as $message) {
                        $this->addFlash('error', "$field: $message");
                    }
                }
            }
        }

        return $this->render('security/register.html.twig');
    }

    #[Route('/logout', name: 'app_logout', methods: ['GET'])]
    public function logout(SessionInterface $session): Response
    {
        // ✅ Nettoyage session
        $session->remove('jwt_token');
        $session->remove('jwt_refresh');
        $session->remove('user');

        $this->addFlash('success', 'Logout successful');
    return $this->redirectToRoute('app_login');
    }

    // ✅ NOUVEAU: endpoint que la navbar va interroger
    #[Route('/auth/status', name: 'auth_status', methods: ['GET'])]
    public function status(Request $request): JsonResponse
    {
        $session = $request->getSession();
        $loggedIn = $session->has('jwt_token');

        return $this->json([
            'loggedIn' => $loggedIn,
            // on renvoie un mini profil si dispo (optionnel)
            'user' => $loggedIn ? $session->get('user') : null,
        ]);
    }
}
