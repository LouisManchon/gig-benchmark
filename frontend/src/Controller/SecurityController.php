<?php

namespace App\Controller;

use App\Service\AuthService;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
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
        // Si déjà connecté, redirige vers home
        if ($session->has('jwt_token')) {
            return $this->redirectToRoute('home');
        }

        if ($request->isMethod('POST')) {
            $username = $request->request->get('username');
            $password = $request->request->get('password');

            $result = $this->authService->login($username, $password);

            if ($result['success']) {
                // 🔥 STOCKE LES TOKENS EN SESSION
                $session->set('jwt_token', $result['access']);
                $session->set('jwt_refresh', $result['refresh']);

                $this->addFlash('success', 'Login successful!');
                return $this->redirectToRoute('home');
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

            if ($result['success']) {
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

    #[Route('/logout', name: 'app_logout')]
    public function logout(SessionInterface $session): Response
    {
        // 🔥 SUPPRIME LES TOKENS DE LA SESSION
        $session->remove('jwt_token');
        $session->remove('jwt_refresh');

        $this->addFlash('success', 'Logout successful');
        return $this->redirectToRoute('app_login');
    }
}
