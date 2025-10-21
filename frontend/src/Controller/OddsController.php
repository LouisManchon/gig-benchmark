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
        $sportChoices = [];
        $bookmakerChoices = [];
        $matchChoices = [];
        $leagueChoices = [];

        try {
            // --- Récupération des données pour les filtres ---
            $sportsArray = $apiService->getDistinctSports();
            $bookmakersArray = $apiService->getDistinctBookmakers();
            $matchesArray = $apiService->getDistinctMatches();
            $leaguesArray = $apiService->getDistinctLeagues();
            
            // Transform match
            if (is_array($sportsArray)) {
                foreach ($sportsArray as $sport) {
                    if (isset($sport['name']) && isset($sport['id'])) {
                        $sportChoices[$sport['name']] = (string)$sport['id'];
                    }
                }
            }
            // Transformer les bookmakers
            if (is_array($bookmakersArray)) {
                foreach ($bookmakersArray as $bookmaker) {
                    if (isset($bookmaker['name']) && isset($bookmaker['id'])) {
                        $bookmakerChoices[$bookmaker['name']] = (string)$bookmaker['id'];
                    }
                }
            }

            // Transformer les matches
            if (is_array($matchesArray)) {
                foreach ($matchesArray as $match) {
                    $matchName = ($match['home_team']['name'] ?? 'Unknown') . ' - ' . ($match['away_team']['name'] ?? 'Unknown');
                    $matchChoices[$matchName] = (string)$match['id'];
                }
            }

            // Transformer les leagues
            if (is_array($leaguesArray)) {
                foreach ($leaguesArray as $league) {
                    if (isset($league['name']) && isset($league['id'])) {
                        $leagueChoices[$league['name']] = (string)$league['id'];
                    }
                }
            }

        } catch (\Exception $e) {
            error_log('Error fetching filter data: ' . $e->getMessage());
            $this->addFlash('error', 'Erreur lors du chargement des filtres');
        }

        try {
            // --- Récupération des données ---
            $sportsArray = [$apiService->getDistinctSports()];  // ✅ Nouveau
            error_log('Sports received: ' . json_encode($sportsArray));
            $bookmakersArray = $apiService->getDistinctBookmakers();
            $matchesArray = $apiService->getDistinctMatches();
            $leaguesArray = $apiService->getDistinctLeagues();

            // Sports (sans "Tous")
            if (is_array($sportsArray)) {
                foreach ($sportsArray as $sport) {
                    if (isset($sport['name']) && isset($sport['id'])) {
                        $sportChoices[$sport['name']] = (string)$sport['id'];
                    }
                }
            }

            // Bookmakers (sans "Tous")
            if (is_array($bookmakersArray)) {
                foreach ($bookmakersArray as $bookmaker) {
                    if (isset($bookmaker['name']) && isset($bookmaker['id'])) {
                        $bookmakerChoices[$bookmaker['name']] = (string)$bookmaker['id'];
                    }
                }
            }

            // Matches (sans "Tous")
            if (is_array($matchesArray)) {
                foreach ($matchesArray as $match) {
                    $matchName = ($match['home_team']['name'] ?? 'Unknown') . ' - ' . ($match['away_team']['name'] ?? 'Unknown');
                    $matchChoices[$matchName] = (string)$match['id'];
                }
            }

            // Leagues avec sport_id pour le filtrage JS
            if (is_array($leaguesArray)) {
                foreach ($leaguesArray as $league) {
                    if (isset($league['name']) && isset($league['id'])) {
                        // ✅ Stocke l'ID du sport dans l'attribut data
                        $leagueChoices[$league['name']] = (string)$league['id'];
                    }
                }
            }

            // --- Création du formulaire (toujours, même si erreur API) ---
            $form = $this->createForm(OddsFilterType::class, null, [
                'method' => 'GET',
                'sports' => $sportChoices,
                'bookmakers' => $bookmakerChoices,
                'matches' => $matchChoices,
                'leagues' => $leagueChoices,
            ]);
            
            $form->handleRequest($request);

            // --- Préparation des filtres ---
            $filters = [];
            
            if ($form->isSubmitted()) {
                error_log('Form is submitted');
                
                if ($form->isValid()) {
                    error_log('Form is valid');
                    
                    $sportFilter = $form->get('sport')->getData();
                    $bookmakerFilter = $form->get('bookmaker')->getData();
                    $matchFilter = $form->get('match')->getData();
                    $leagueFilter = $form->get('league')->getData();
                    $dateRange = $form->get('dateRange')->getData();

                    error_log('Bookmaker filter: ' . json_encode($bookmakerFilter));
                    error_log('Match filter: ' . json_encode($matchFilter));
                    error_log('League filter: ' . json_encode($leagueFilter));
                    error_log('Date range: ' . $dateRange);
                    
                    //Sport

                    if ($sportFilter) {
                        $filters['sport'] = $sportFilter;
                    }
                    // Bookmaker (multiple)
                    if ($bookmakerFilter && is_array($bookmakerFilter)) {
                        // Enlève 'all' du tableau
                        $bookmakerFilter = array_filter($bookmakerFilter, fn($v) => $v !== 'all');
                        if (!empty($bookmakerFilter)) {
                            $filters['bookmaker'] = implode(',', $bookmakerFilter);
                        }
                    }
                    
                    // Match (simple)
                    if ($matchFilter && $matchFilter !== 'all' && $matchFilter !== '') {
                        $filters['match'] = $matchFilter;
                    }
                    
                    // League (multiple)
                    if ($leagueFilter && is_array($leagueFilter)) {
                        $leagueFilter = array_filter($leagueFilter, fn($v) => $v !== 'all');
                        if (!empty($leagueFilter)) {
                            $filters['league'] = implode(',', $leagueFilter);
                        }
                    }

                    // Date range
                    if ($dateRange && trim($dateRange) !== '') {
                        if (str_contains($dateRange, ' to ')) {
                            $dates = explode(' to ', $dateRange);
                        } else {
                            $dates = [$dateRange];
                        }
                        
                        try {
                            $start = new \DateTime(trim($dates[0]), new \DateTimeZone('UTC'));
                            $start->setTime(0, 0, 0);
                            
                            if (isset($dates[1])) {
                                $end = new \DateTime(trim($dates[1]), new \DateTimeZone('UTC'));
                                $end->setTime(23, 59, 59);
                            } else {
                                $end = clone $start;
                                $end->setTime(23, 59, 59);
                            }
                            
                            $filters['start'] = $start->format('Y-m-d H:i:s');
                            $filters['end'] = $end->format('Y-m-d H:i:s');
                        } catch (\Exception $e) {
                            error_log('Date error: ' . $e->getMessage());
                        }
                    }
      
                    error_log('Final filters: ' . json_encode($filters));
                } else {
                    error_log('Form is NOT valid');
                    $errors = [];
                    foreach ($form->getErrors(true) as $error) {
                        $errors[] = $error->getMessage();
                    }
                    error_log('Form errors: ' . json_encode($errors));
                }
            } else {
                error_log('Form is NOT submitted');
            }

            // --- Récupération des données ---
            $allOdds = $apiService->getOddsWithFilters($filters);
            $avgTrjRaw = $apiService->getAvgTrj($filters);

            // --- Regroupement des cotes par match + bookmaker ---
            $groupedOdds = [];
            if (is_array($allOdds)) {
                foreach ($allOdds as $odd) {
                    $matchId = $odd['match']['id'] ?? 0;
                    $bookmakerId = $odd['bookmaker']['id'] ?? 0;
                    $key = $matchId . '_' . $bookmakerId;
                    
                    if (!isset($groupedOdds[$key])) {
                        $groupedOdds[$key] = [
                            'match' => $odd['match'],
                            'bookmaker' => $odd['bookmaker'],
                            'trj' => $odd['trj'] ?? 0,
                            'cotes' => ['1' => null, 'X' => null, '2' => null]
                        ];
                    }
                    
                    $outcome = $odd['outcome'] ?? '';
                    if (in_array($outcome, ['1', 'X', '2'])) {
                        $groupedOdds[$key]['cotes'][$outcome] = $odd['odd_value'] ?? 0;
                    }
                }
            }

            // --- Prépare pour l'affichage ---
            foreach ($groupedOdds as $grouped) {
                $oddsWithEvolution[] = [
                    'odd' => [
                        'match' => $grouped['match'],
                        'bookmaker' => $grouped['bookmaker'],
                        'cote1' => $grouped['cotes']['1'],
                        'coteN' => $grouped['cotes']['X'],
                        'cote2' => $grouped['cotes']['2'],
                        'trj' => $grouped['trj']
                    ],
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

        } catch (\Exception $e) {
            $this->addFlash('error', 'Erreur : ' . $e->getMessage());
            error_log('Controller error: ' . $e->getMessage());
            error_log('Stack trace: ' . $e->getTraceAsString());
        }

        // --- Rendu (toujours avec $form, même si null) ---
        return $this->render('odds/index.html.twig', [
            'form' => $form ? $form->createView() : null,
            'odds' => $oddsWithEvolution,
            'oddsWithEvolution' => $oddsWithEvolution,
            'avgTrj' => $avgTrj,
            'leaguesData' => json_encode($leaguesArray ?? []),
        ]);
    }
}
