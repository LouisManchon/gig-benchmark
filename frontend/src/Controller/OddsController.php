<?php

// src/Controller/OddsController.php
namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use App\Service\DjangoApiService;

class OddsController extends AbstractController
{
    #[Route('/odds', name: 'odds_list')]
    public function index(Request $request, DjangoApiService $api): Response
    {
        $data = $api->getDistinctBookmakers(); // Exemple d'appel au service
        return $this->json($data); // Retourne les données en JSON pour tester
    }
}
