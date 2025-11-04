<?php

namespace App\Controller;

use App\Form\OddsFilterType;
use App\Service\OddsApiService;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Session\SessionInterface;
use Symfony\Component\HttpFoundation\StreamedResponse;
use Symfony\Component\Routing\Annotation\Route;

class OddsController extends AbstractController
{
    #[Route('/', name: 'home')]
    #[Route('/odds', name: 'odds_list')]
    public function index(Request $request, OddsApiService $apiService, SessionInterface $session): Response
    {
        if (!$session->has('jwt_token')) {
            $this->addFlash('error', 'You must be logged in to access this page.');
            return $this->redirectToRoute('app_login');
        }

        $token = $session->get('jwt_token');

        // Initialisation par défaut
        $form = null;
        $oddsWithEvolution = [];
        $avgTrj = [];
        $sportChoices = [];
        $bookmakerChoices = [];
        $matchChoices = [];
        $leagueChoices = [];
        $startTime = microtime(true);
        error_log("⏱️ START - index()");

        try {
            // --- Récupération des données pour les filtres ---
            $sportsArray = $apiService->getDistinctSports();
            $bookmakersArray = $apiService->getDistinctBookmakers();
            $matchesArray = $apiService->getDistinctMatches();
            $leaguesArray = $apiService->getDistinctLeagues();
            
            // Transform sports
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
            // --- Valeur par défaut pour dateRange ---
            $today = new \DateTime('now', new \DateTimeZone('UTC'));
            $defaultDateRange = $today->format('Y-m-d');  // Format pour flatpickr

            // --- Création du formulaire ---
            $form = $this->createForm(OddsFilterType::class, [
                'dateRange' => $defaultDateRange  // Pré-remplir avec la date du jour
            ], [
                'method' => 'GET',
                'sports' => $sportChoices,
                'bookmakers' => $bookmakerChoices,
                'leagues' => $leagueChoices,
                'matches' => $matchChoices,
            ]);
            
            $form->handleRequest($request);
            error_log("⏱️ Form created: " . round((microtime(true) - $startTime) * 1000, 2) . "ms");

            // --- Préparation des filtres ---
            $filters = [];

            // Définir la date du jour par défaut si aucun filtre n'est soumis
            $defaultDateApplied = false;
            if (!$form->isSubmitted()) {
                $today = new \DateTime('now', new \DateTimeZone('UTC'));
                $today->setTime(0, 0, 0);
                $todayEnd = clone $today;
                $todayEnd->setTime(23, 59, 59);

                $filters['start'] = $today->format('Y-m-d H:i:s');
                $filters['end'] = $todayEnd->format('Y-m-d H:i:s');
                $defaultDateApplied = true;

                error_log('📅 Default date filter applied: ' . $filters['start'] . ' to ' . $filters['end']);
            }

            if ($form->isSubmitted() && $form->isValid()) {
                $sportFilter = $form->get('sport')->getData();
                $bookmakerFilter = $form->get('bookmaker')->getData();
                $matchFilter = $form->get('match')->getData();
                $leagueFilter = $form->get('league')->getData();
                $dateRange = $form->get('dateRange')->getData();

                error_log('🔍 Match filter value: ' . var_export($matchFilter, true));

                // Sport
                if ($sportFilter) {
                    $filters['sport'] = $sportFilter;
                }
                
                // Bookmaker (multiple)
                if ($bookmakerFilter && is_array($bookmakerFilter)) {
                    $bookmakerFilter = array_filter($bookmakerFilter, fn($v) => $v !== 'all');
                    if (!empty($bookmakerFilter)) {
                        $filters['bookmaker'] = implode(',', $bookmakerFilter);
                    }
                }
                
                // Match (simple)
                if ($matchFilter && $matchFilter !== 'all' && $matchFilter !== '') {
                    error_log('🔍 MATCH FILTER DETECTED: ' . $matchFilter);
                    
                    if (is_numeric($matchFilter)) {
                        $filters['match'] = $matchFilter;
                        error_log('   → Filtering by ID: ' . $matchFilter);
                    } else {
                        $filters['match_name'] = $matchFilter;
                        error_log('   → Filtering by name: ' . $matchFilter);
                    }
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
                        $defaultDateApplied = false; // Date explicitement fournie
                    } catch (\Exception $e) {
                        error_log('Date error: ' . $e->getMessage());
                    }
                } else if ($form->isSubmitted()) {
                    // Si le formulaire est soumis SANS date, ne pas appliquer de filtre de date
                    unset($filters['start']);
                    unset($filters['end']);
                    $defaultDateApplied = false;
                }
            }
            error_log("⏱️ Filters prepared: " . round((microtime(true) - $startTime) * 1000, 2) . "ms");

            error_log('🔍 Filtres appliqués: ' . json_encode($filters));

            // --- Récupération des données AVEC évolution ---
            $allOdds = $apiService->getOddsWithEvolution($filters);

            error_log("⏱️ API called (odds): " . round((microtime(true) - $startTime) * 1000, 2) . "ms");
            error_log("   → Found " . count($allOdds) . " odds");

            $avgTrjRaw = $apiService->getAvgTrjWithEvolution($filters);

            error_log("⏱️ API called (avgTrj): " . round((microtime(true) - $startTime) * 1000, 2) . "ms");
            error_log("   → Found " . count($avgTrj) . " bookmakers");

            error_log('📊 AvgTrjRaw reçu: ' . json_encode($avgTrjRaw));
            error_log('📊 Nombre de bookmakers: ' . count($avgTrjRaw));



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
                            'previous_trj' => $odd['previous_trj'] ?? null,
                            'cotes' => ['1' => null, 'X' => null, '2' => null]
                        ];
                    } else {
                        // Mise à jour du previous_trj si on en trouve un
                        if (isset($odd['previous_trj'])) {
                            $groupedOdds[$key]['previous_trj'] = $odd['previous_trj'];
                        }
                    }
                    
                    $outcome = $odd['outcome'] ?? '';
                    if (in_array($outcome, ['1', 'X', '2'])) {
                        $groupedOdds[$key]['cotes'][$outcome] = $odd['odd_value'] ?? 0;
                    }
                }
            }

            // --- Prépare pour l'affichage avec calcul de l'évolution ---
            foreach ($groupedOdds as $grouped) {
                $currentTrj = $grouped['trj'];
                $previousTrj = $grouped['previous_trj'];
                
                // Calcul de l'évolution : 1 = hausse, -1 = baisse, 0 = stable/pas de donnée
                $evolution = 0;
                if ($previousTrj !== null && $previousTrj > 0) {
                    if ($currentTrj > $previousTrj) {
                        $evolution = 1;
                    } elseif ($currentTrj < $previousTrj) {
                        $evolution = -1;
                    }
                }
                
                $oddsWithEvolution[] = [
                    'odd' => [
                        'match' => $grouped['match'],
                        'bookmaker' => $grouped['bookmaker'],
                        'cote1' => $grouped['cotes']['1'],
                        'coteN' => $grouped['cotes']['X'],
                        'cote2' => $grouped['cotes']['2'],
                        'trj' => $currentTrj
                    ],
                    'previousTrj' => $previousTrj,
                    'evolution' => $evolution
                ];
            }

            // --- Formatage des moyennes TRJ avec évolution ---
            if (is_array($avgTrjRaw)) {
                foreach ($avgTrjRaw as $row) {
                    $currentAvgTrj = isset($row['avg_trj']) ? round((float)$row['avg_trj'], 2) : 0;
                    $previousAvgTrj = isset($row['previous_avg_trj']) && $row['previous_avg_trj'] !== null 
                        ? round((float)$row['previous_avg_trj'], 2) 
                        : null;
                    
                    // Calcul de l'évolution
                    $evolution = 0;
                    if ($previousAvgTrj !== null && $previousAvgTrj > 0) {
                        if ($currentAvgTrj > $previousAvgTrj) {
                            $evolution = 1;
                        } elseif ($currentAvgTrj < $previousAvgTrj) {
                            $evolution = -1;
                        }
                    }
                    
                    $avgTrj[] = [
                        'bookmaker' => $row['bookmaker__name'] ?? 'Unknown',
                        'avgTrj' => $currentAvgTrj,
                        'previousAvgTrj' => $previousAvgTrj,
                        'evolution' => $evolution,
                    ];
                }
            }

            error_log('✅ Données préparées - OddsWithEvolution: ' . count($oddsWithEvolution) . ', AvgTrj: ' . count($avgTrj));

        } catch (\Exception $e) {
            $this->addFlash('error', 'Erreur : ' . $e->getMessage());
            error_log('❌ Controller error: ' . $e->getMessage());
            error_log('Stack trace: ' . $e->getTraceAsString());
        }

        $totalTime = round((microtime(true) - $startTime) * 1000, 2);
        error_log("⏱️ TOTAL TIME: {$totalTime}ms");

        // --- Récupération de la dernière date de scraping ---
        $lastScrapingDate = null;
        try {
            $lastScrapingDate = $apiService->getLastScrapingDate();
        } catch (\Exception $e) {
            error_log('❌ Error fetching last scraping date: ' . $e->getMessage());
        }

        // --- Rendu ---
        return $this->render('odds/index.html.twig', [
            'form' => $form ? $form->createView() : null,
            'odds' => $oddsWithEvolution,
            'oddsWithEvolution' => $oddsWithEvolution,
            'avgTrj' => $avgTrj,
            'leaguesData' => json_encode($leaguesArray ?? []),
            'matchesData' => json_encode($matchesArray ?? []),
            'lastScrapingDate' => $lastScrapingDate,
        ]);
    }

    #[Route('/odds/export-csv', name: 'odds_export_csv', methods: ['GET'])]
    public function exportCsv(Request $request, OddsApiService $apiService): Response
    {
        try {
            $filters = [];
            
            $sportFilter = $request->query->get('sport');
            $bookmakerFilter = $request->query->get('bookmaker');
            $matchFilter = $request->query->get('match');
            $leagueFilter = $request->query->get('league');
            $dateRange = $request->query->get('dateRange');

            if ($sportFilter && $sportFilter !== 'all') {
                $filters['sport'] = $sportFilter;
            }
            
            if ($bookmakerFilter && $bookmakerFilter !== 'all') {
                $filters['bookmaker'] = $bookmakerFilter;
            }
            
            if ($matchFilter && $matchFilter !== 'all') {
                $filters['match'] = $matchFilter;
            }
            
            if ($leagueFilter && $leagueFilter !== 'all') {
                $filters['league'] = $leagueFilter;
            }

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

            // Utilise la méthode normale pour l'export (pas besoin de l'évolution dans le CSV)
            $allOdds = $apiService->getOddsWithFilters($filters);

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
                            'cotes' => ['1' => null, 'X' => null, '2' => null],
                            'date' => $odd['match']['match_date'] ?? ''
                        ];
                    }
                    
                    $outcome = $odd['outcome'] ?? '';
                    if (in_array($outcome, ['1', 'X', '2'])) {
                        $groupedOdds[$key]['cotes'][$outcome] = $odd['odd_value'] ?? 0;
                    }
                }
            }

            $response = new StreamedResponse(function() use ($groupedOdds) {
                $handle = fopen('php://output', 'w');
                
                // BOM UTF-8 pour Excel
                fprintf($handle, chr(0xEF).chr(0xBB).chr(0xBF));
                
                fputcsv($handle, [
                    'Date',
                    'Match',
                    'Home Team',
                    'Away team',
                    'Bookmaker',
                    'Home',
                    'Draw',
                    'Away',
                    'RTP (%)'
                ], ';');

                foreach ($groupedOdds as $grouped) {
                    $matchDate = '';
                    if (!empty($grouped['date'])) {
                        try {
                            $dateObj = new \DateTime($grouped['date']);
                            $matchDate = "\t" . $dateObj->format('d/m/Y H:i');
                        } catch (\Exception $e) {
                            $matchDate = '';
                        }
                    }

                    fputcsv($handle, [
                        $matchDate,
                        ($grouped['match']['home_team']['name'] ?? '') . ' - ' . ($grouped['match']['away_team']['name'] ?? ''),
                        $grouped['match']['home_team']['name'] ?? '',
                        $grouped['match']['away_team']['name'] ?? '',
                        $grouped['bookmaker']['name'] ?? '',
                        $grouped['cotes']['1'] ?? '-',
                        $grouped['cotes']['X'] ?? '-',
                        $grouped['cotes']['2'] ?? '-',
                        number_format($grouped['trj'], 2, ',', '')
                    ], ';');
                }

                fclose($handle);
            });

            $filename = 'odds_export_' . date('Y-m-d_His') . '.csv';
            $response->headers->set('Content-Type', 'text/csv; charset=utf-8');
            $response->headers->set('Content-Disposition', 'attachment; filename="' . $filename . '"');
            
            return $response;

        } catch (\Exception $e) {
            $this->addFlash('error', 'Erreur lors de l\'export CSV : ' . $e->getMessage());
            return $this->redirectToRoute('odds_list');
        }
    }

    #[Route('/odds/scraping/trigger', name: 'scraping_trigger', methods: ['POST'])]
    public function triggerScraping(Request $request, OddsApiService $apiService): Response
    {
        try {
        $sport = $request->request->get('sport') ?? $request->request->get('scraping_sport');
        $league = $request->request->get('league') ?? $request->request->get('scraping_league');
            
            if (!$sport || !$league) {
                return $this->json([
                    'success' => false,
                    'error' => 'Sport et league requis'
                ], 400);
            }
            
            // Construire le nom du scraper (ex: football.ligue_1)
            $scraper = $sport . '.' . str_replace(' ', '_', strtolower($league));
            
            error_log("🚀 Déclenchement du scraping: $scraper");
            
            // Appeler l'API Django
            $result = $apiService->triggerScraping($scraper);
            
            if ($result['success'] ?? false) {
                return $this->json([
                    'success' => true,
                    'message' => 'Scraping en cours...'
                ]);
            } else {
                return $this->json([
                    'success' => false,
                    'error' => $result['error'] ?? 'Erreur inconnue'
                ], 500);
            }
            
        } catch (\Exception $e) {
            error_log('❌ Erreur scraping: ' . $e->getMessage());
            return $this->json([
                'success' => false,
                'error' => $e->getMessage()
            ], 500);
        }
    }

    #[Route('/api/scraping/status', name: 'scraping_status_proxy', methods: ['GET'])]
    public function getScrapingStatus(Request $request, OddsApiService $apiService): Response
    {
        $scraper = $request->query->get('scraper');
        
        if (!$scraper) {
            return $this->json([
                'status' => 'idle',
                'current' => 0,
                'total' => 0,
                'message' => 'Pas de scraping en cours'
            ]);
        }
        
        try {
            // Appelle le backend Django via le service
            $backendUrl = $_ENV['BACKEND_API_URL'] ?? 'http://backend:8000/api';
            $url = $backendUrl . '/scraping/status?scraper=' . urlencode($scraper);
            
            $context = stream_context_create([
                'http' => [
                    'method' => 'GET',
                    'timeout' => 3,
                    'ignore_errors' => true
                ]
            ]);
            
            $response = @file_get_contents($url, false, $context);
            
            if ($response) {
                $data = json_decode($response, true);
                return $this->json($data);
            }
            
            // Si pas de réponse, retourne idle
            return $this->json([
                'status' => 'idle',
                'current' => 0,
                'total' => 0
            ]);
            
        } catch (\Exception $e) {
            return $this->json([
                'status' => 'idle',
                'current' => 0,
                'total' => 0
            ]);
        }
    }

    #[Route('/api/scraping/auto/status', name: 'auto_scraping_status', methods: ['GET'])]
    public function getAutoScrapingStatus(Request $request): Response
    {
        try {
            $backendUrl = $_ENV['BACKEND_API_URL'] ?? 'http://backend:8000/api';
            $url = $backendUrl . '/scraping/auto/status';

            $context = stream_context_create([
                'http' => [
                    'method' => 'GET',
                    'timeout' => 5,
                    'ignore_errors' => true
                ]
            ]);

            $response = @file_get_contents($url, false, $context);

            if ($response) {
                $data = json_decode($response, true);
                return $this->json($data);
            }

            return $this->json([
                'success' => false,
                'error' => 'Backend unreachable'
            ], 500);

        } catch (\Exception $e) {
            return $this->json([
                'success' => false,
                'error' => $e->getMessage()
            ], 500);
        }
    }

    #[Route('/api/scraping/auto/toggle', name: 'toggle_auto_scraping', methods: ['POST'])]
    public function toggleAutoScraping(Request $request): Response
    {
        try {
            $data = json_decode($request->getContent(), true);
            $enabled = $data['enabled'] ?? null;

            if ($enabled === null) {
                return $this->json([
                    'success' => false,
                    'error' => 'enabled parameter required'
                ], 400);
            }

            $backendUrl = $_ENV['BACKEND_API_URL'] ?? 'http://backend:8000/api';
            $url = $backendUrl . '/scraping/auto/toggle';

            $context = stream_context_create([
                'http' => [
                    'method' => 'POST',
                    'header' => 'Content-Type: application/json',
                    'content' => json_encode(['enabled' => $enabled]),
                    'timeout' => 5,
                    'ignore_errors' => true
                ]
            ]);

            $response = @file_get_contents($url, false, $context);

            if ($response) {
                $responseData = json_decode($response, true);
                return $this->json($responseData);
            }

            return $this->json([
                'success' => false,
                'error' => 'Backend unreachable'
            ], 500);

        } catch (\Exception $e) {
            return $this->json([
                'success' => false,
                'error' => $e->getMessage()
            ], 500);
        }
    }
}
