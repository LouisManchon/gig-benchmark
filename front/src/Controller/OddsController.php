<?php

namespace App\Controller;

use App\Form\OddsFilterType;
use App\Repository\OddRepository;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class OddsController extends AbstractController
{
    #[Route('/', name: 'home')]
    #[Route('/odds', name: 'odds_list')]
    public function index(Request $request, OddRepository $oddRepository): Response
    {
        // --- Récupération des filtres distincts ---
        $bookmakersArray = $oddRepository->findDistinctBookmakers();
        $matchesArray = $oddRepository->findDistinctMatches();
        $leaguesArray = $oddRepository->findDistinctLeagues();

        // --- Création du formulaire ---
        $form = $this->createForm(OddsFilterType::class, null, [
            'method' => 'GET',
            'bookmakers' => $bookmakersArray,
            'matches' => $matchesArray,
            'leagues' => $leaguesArray,
        ]);
        $form->handleRequest($request);

        // --- Récupération des valeurs filtrées ---
        $bookmakerFilter = [];
        $matchFilter = null;
        $leagueFilter = null;
        $start = null;
        $end = null;

        if ($form->isSubmitted() && $form->isValid()) {
            $bookmakerFilter = $form->get('bookmaker')->getData() ?? [];
            $matchFilter = $form->get('match')->getData();
            $leagueFilter = $form->get('league')->getData();
            $dateRange = $form->get('dateRange')->getData();

            if (is_array($bookmakerFilter) && in_array('all', $bookmakerFilter)) {
                $bookmakerFilter = [];
            }

            if ($dateRange) {
                $dates = str_contains($dateRange, ' to ') ? explode(' to ', $dateRange) : [$dateRange];
                try {
                    $start = new \DateTime(trim($dates[0]) . ' 00:00:00');
                    $end = isset($dates[1]) ? new \DateTime(trim($dates[1]) . ' 23:59:59') : new \DateTime(trim($dates[0]) . ' 23:59:59');
                } catch (\Exception $e) {
                    $start = null;
                    $end = null;
                }
            }
        }

        // --- Récupération des cotes filtrées ---
        $allOdds = $oddRepository->findWithFilters($bookmakerFilter, $leagueFilter, $matchFilter, $start, $end);

        // --- Latest odds par match + bookmaker ---
        $latestOdds = [];
        foreach ($allOdds as $odd) {
            $key = $odd->getMatchName() . '|' . $odd->getBookmaker();
            if (!isset($latestOdds[$key])) {
                $latestOdds[$key] = $odd;
            }
        }

        // --- Calcul de l'évolution TRJ pour chaque cote ---
        $oddsWithEvolution = [];
        foreach ($latestOdds as $currentOdd) {
            $previousOdd = $oddRepository->findPreviousOdd(
                $currentOdd->getMatchName(),
                $currentOdd->getBookmaker(),
                $currentOdd->getCreatedAt()
            );

            $evolution = 0; // 0 = stable, 1 = hausse, -1 = baisse
            $previousTrj = null;

            if ($previousOdd) {
                $previousTrj = $previousOdd->getTrj();
                $diff = $currentOdd->getTrj() - $previousTrj;
                if ($diff > 0.1) $evolution = 1;
                elseif ($diff < -0.1) $evolution = -1;
            }

            $oddsWithEvolution[] = [
                'odd' => $currentOdd,
                'previousTrj' => $previousTrj,
                'evolution' => $evolution
            ];
        }

        // --- Moyenne TRJ par bookmaker ---
        $avgTrjRaw = $oddRepository->findAvgTrj($bookmakerFilter, $leagueFilter, $matchFilter, $start, $end);

        // --- Calcul évolution moyenne TRJ et ancien TRJ ---
        $lastScrapingDate = $oddRepository->findLastScrapingDate();
        $previousScrapingDate = $lastScrapingDate ? $oddRepository->findPreviousScrapingDate($lastScrapingDate) : null;

        // Dans le Controller, remplace toute la section avgTrj par :

        // --- Moyenne TRJ par bookmaker ---
        $avgTrjRaw = $oddRepository->findAvgTrj($bookmakerFilter, $leagueFilter, $matchFilter, $start, $end);

        $avgTrj = [];
        foreach ($avgTrjRaw as $row) {
            $evolution = 0;
            $previousAvgTrj = null;

            // Récupérer le TRJ moyen du scraping précédent pour ce bookmaker
            $previousOdds = $oddRepository->findPreviousAvgForBookmaker($row['bookmaker']);
            
            if ($previousOdds) {
                $previousAvgTrj = $previousOdds;
                $diff = $row['avgTrj'] - $previousAvgTrj;
                if ($diff > 0.1) $evolution = 1;
                elseif ($diff < -0.1) $evolution = -1;
            }

            $avgTrj[] = [
                'bookmaker' => $row['bookmaker'],
                'avgTrj' => $row['avgTrj'],
                'previousAvgTrj' => $previousAvgTrj,
                'evolution' => $evolution,
            ];
        }

        // --- Rendu du template ---
        return $this->render('odds/index.html.twig', [
            'form' => $form->createView(),
            'odds' => $oddsWithEvolution,
            'oddsWithEvolution' => $oddsWithEvolution,
            'avgTrj' => $avgTrj,
        ]);
    }
}
