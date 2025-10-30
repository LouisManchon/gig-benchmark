<?php

namespace App\Controller;

use App\Service\AuthService;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Cookie;
use Symfony\Component\Routing\Annotation\Route;

class SecurityController extends AbstractController
{
    private AuthService $authService;

    public function __construct(AuthService $authService)
    {
        $this->authService = $authService;
    }

    #[Route('/login', name: 'app_login')]
    public function login(Request $request): Response
    {
        // Si déjà connecté, redirige vers la home
        if ($request->cookies->has('jwt_token')) {
            return $this->redirectToRoute('home');
        }

        if ($request->isMethod('POST')) {
            $username = $request->request->get('username');
            $password = $request->request->get('password');

            $result = $this->authService->login($username, $password);

            if ($result['success']) {
                $response = $this->redirectToRoute('home');

                // Stocke le token dans un cookie sécurisé
                $response->headers->setCookie(
                    Cookie::create('jwt_token')
                        ->withValue($result['token'])
                        ->withExpires(strtotime('+1 hour'))
                        ->withPath('/')
                        ->withSecure(false) // true en production avec HTTPS
                        ->withHttpOnly(true)
                );

                // Stocke le refresh token
                $response->headers->setCookie(
                    Cookie::create('jwt_refresh')
                        ->withValue($result['refresh'])
                        ->withExpires(strtotime('+7 days'))
                        ->withPath('/')
                        ->withSecure(false)
                        ->withHttpOnly(true)
                );

                $this->addFlash('success', 'Connexion réussie !');
                return $response;
            }

            $this->addFlash('error', $result['error'] ?? 'Identifiants invalides');
        }

        return $this->render('security/login.html.twig');
    }

    #[Route('/register', name: 'app_register')]
    public function register(Request $request): Response
    {
        if ($request->cookies->has('jwt_token')) {
            return $this->redirectToRoute('home');
        }

        if ($request->isMethod('POST')) {
            $userData = [
                'username' => $request->request->get('username'),
                'email' => $request->request->get('email'),
                'password' => $request->request->get('password'),
                'password2' => $request->request->get('password2'),
            ];

            $result = $this->authService->register($userData);

            if ($result['success']) {
                $this->addFlash('success', 'Inscription réussie ! Vous pouvez maintenant vous connecter.');
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
    public function logout(): Response
    {
        $response = $this->redirectToRoute('app_login');

        // Supprime les cookies
        $response->headers->clearCookie('jwt_token');
        $response->headers->clearCookie('jwt_refresh');

        $this->addFlash('success', 'Déconnexion réussie');
        return $response;
    }
}
