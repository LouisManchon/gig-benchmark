<?php
namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Session\SessionInterface;
use Symfony\Component\Routing\Annotation\Route;

class HomeController extends AbstractController
{
    #[Route('/', name: 'home')]
    public function index(SessionInterface $session): Response
    {
        // 🔐 Si pas de token -> redirige login
        if (!$session->has('jwt_token')) {
            return $this->redirectToRoute('app_login');
        }

        // ✅ Si connecté -> redirige vers odds
        return $this->redirectToRoute('odds_list');
    }
}