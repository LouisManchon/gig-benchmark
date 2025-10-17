<?php

namespace App\Controller;

use App\Form\OddsFilterType;
use App\Service\OddsApiService;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class OddsController extends AbstractController
{
    #[Route('/', name: 'home')]
    #[Route('/odds', name: 'odds_list')]
    public function index(Request $request, OddsApiService $apiService): Response
    {
        // Initialisation par défaut
        $form = null;
        $oddsWithEvolution = [];
        $avgTrj = [];

        try {
            // --- Récupération des données pour les filtres ---
            $bookmakersArray = $apiService->getDistinctBookmakers();
            $matchesArray = $apiService->getDistinctMatches();
            $leaguesArray = $apiService->getDistinctLeagues();

            // Debug : affiche les données reçues
            error_log('Bookmakers: ' . json_encode($bookmakersArray));
            error_log('Matches: ' . json_encode($matchesArray));
            error_log('Leagues: ' . json_encode($leaguesArray));

            // Transformer les données API en format pour le formulaire
            $bookmakerChoices = ['Tous' => 'all'];
            if (is_array($bookmakersArray)) {
                foreach ($bookmakersArray as $bookmaker) {
                    if (isset($bookmaker['name']) && isset($bookmaker['id'])) {
                        $bookmakerChoices[$bookmaker['name']] = (string)$bookmaker['id'];
                    }
                }
            }

            $matchChoices = ['Tous' => ''];
            if (is_array($matchesArray)) {
                foreach ($matchesArray as $match) {
                    if (isset($match['name']) && isset($match['id'])) {
                        $matchChoices[$match['name']] = (string)$match['id'];
                    }
                }
            }

            $leagueChoices = ['Toutes' => ''];
            if (is_array($leaguesArray)) {
                foreach ($leaguesArray as $league) {
                    if (isset($league['name']) && isset($league['id'])) {
                        $leagueChoices[$league['name']] = (string)$league['id'];
                    }
                }
            }

            // --- Création du formulaire ---
            $form = $this->createForm(OddsFilterType::class, null, [
                'method' => 'GET',
                'bookmakers' => $bookmakerChoices,
                'matches' => $matchChoices,
                'leagues' => $leagueChoices,
            ]);
            $form->handleRequest($request);

            // --- Préparation des filtres ---
            $filters = [];
            
            if ($form->isSubmitted() && $form->isValid()) {
                $bookmakerFilter = $form->get('bookmaker')->getData();
                $matchFilter = $form->get('match')->getData();
                $leagueFilter = $form->get('league')->getData();
                $dateRange = $form->get('dateRange')->getData();

                if ($bookmakerFilter && $bookmakerFilter !== 'all') {
                    $filters['bookmaker'] = is_array($bookmakerFilter) ? implode(',', $bookmakerFilter) : $bookmakerFilter;
                }
                if ($matchFilter) {
                    $filters['match'] = $matchFilter;
                }
                if ($leagueFilter) {
                    $filters['league'] = $leagueFilter;
                }

                if ($dateRange) {
                    $dates = str_contains($dateRange, ' to ') ? explode(' to ', $dateRange) : [$dateRange];
                    try {
                        $start = new \DateTime(trim($dates[0]) . ' 00:00:00');
                        $end = isset($dates[1]) ? new \DateTime(trim($dates[1]) . ' 23:59:59') : new \DateTime(trim($dates[0]) . ' 23:59:59');
                        
                        $filters['start'] = $start->format('Y-m-d H:i:s');
                        $filters['end'] = $end->format('Y-m-d H:i:s');
                    } catch (\Exception $e) {
                        error_log('Date parse error: ' . $e->getMessage());
                    }
                }
            }

            // --- Récupération des données ---
            $allOdds = $apiService->getOddsWithFilters($filters);
            $avgTrjRaw = $apiService->getAvgTrj($filters);

            error_log('All odds count: ' . count($allOdds));
            error_log('Avg TRJ count: ' . count($avgTrjRaw));

            // --- Traitement des cotes ---
            $latestOdds = [];
            if (is_array($allOdds)) {
                foreach ($allOdds as $odd) {
                    $matchName = $odd['match']['name'] ?? 'Unknown';
                    $bookmakerName = $odd['bookmaker']['name'] ?? 'Unknown';
                    $key = $matchName . '|' . $bookmakerName;
                    
                    if (!isset($latestOdds[$key])) {
                        $latestOdds[$key] = $odd;
                    }
                }
            }

            foreach ($latestOdds as $currentOdd) {
                $oddsWithEvolution[] = [
                    'odd' => $currentOdd,
                    'previousTrj' => null,
                    'evolution' => 0
                ];
            }

            // --- Formatage des moyennes TRJ ---
            if (is_array($avgTrjRaw)) {
                foreach ($avgTrjRaw as $row) {
                    $avgTrj[] = [
                        'bookmaker' => $row['bookmaker__name'] ?? 'Unknown',
                        'avgTrj' => isset($row['avg_trj']) ? round((float)$row['avg_trj'], 2) : 0,
                        'previousAvgTrj' => null,
                        'evolution' => 0,
                    ];
                }
            }

        } catch (\Symfony\Contracts\HttpClient\Exception\TransportExceptionInterface $e) {
            $this->addFlash('error', 'Impossible de se connecter au backend. Vérifiez que le service backend est démarré.');
            error_log('Transport error: ' . $e->getMessage());
        } catch (\Symfony\Contracts\HttpClient\Exception\ClientExceptionInterface $e) {
            $this->addFlash('error', 'Erreur client HTTP : ' . $e->getMessage());
            error_log('Client error: ' . $e->getMessage());
        } catch (\Exception $e) {
            $this->addFlash('error', 'Erreur : ' . $e->getMessage());
            error_log('General error: ' . $e->getMessage());
            error_log('Stack trace: ' . $e->getTraceAsString());
        }

        // --- Rendu ---
        return $this->render('odds/index.html.twig', [
            'form' => $form ? $form->createView() : null,
            'odds' => $oddsWithEvolution,
            'oddsWithEvolution' => $oddsWithEvolution,
            'avgTrj' => $avgTrj,
        ]);
    }
}
