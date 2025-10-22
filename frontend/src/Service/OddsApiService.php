<?php

namespace App\Service;

use Symfony\Contracts\HttpClient\HttpClientInterface;

class OddsApiService
{
    private HttpClientInterface $httpClient;
    private string $apiBaseUrl;

    public function __construct(HttpClientInterface $httpClient, string $apiBaseUrl)
    {
        $this->httpClient = $httpClient;
        $this->apiBaseUrl = rtrim($apiBaseUrl, '/');
    }

    public function getDistinctSports(): array
    {
        $response = $this->httpClient->request('GET', $this->apiBaseUrl . '/sports');
        return $response->toArray();
    }

    public function getDistinctBookmakers(): array
    {
        $response = $this->httpClient->request('GET', $this->apiBaseUrl . '/bookmakers');
        return $response->toArray();
    }

    public function getDistinctLeagues(): array
    {
        $response = $this->httpClient->request('GET', $this->apiBaseUrl . '/leagues');
        return $response->toArray();
    }

    public function getDistinctMatches(): array
    {
        $response = $this->httpClient->request('GET', $this->apiBaseUrl . '/matches');
        return $response->toArray();
    }

    public function getOddsWithFilters(array $filters = []): array
    {
        $queryParams = [];

        if (!empty($filters['sport'])) {
            $queryParams['sport'] = $filters['sport'];
        }
        if (!empty($filters['bookmaker'])) {
            $queryParams['bookmaker'] = $filters['bookmaker'];
        }
        if (!empty($filters['league'])) {
            $queryParams['league'] = $filters['league'];
        }
        if (!empty($filters['match'])) {
            $queryParams['match'] = $filters['match'];
        }
        if (!empty($filters['start'])) {
            $queryParams['start'] = $filters['start'];
        }
        if (!empty($filters['end'])) {
            $queryParams['end'] = $filters['end'];
        }

        $url = $this->apiBaseUrl . '/odds';
        if (!empty($queryParams)) {
            $url .= '?' . http_build_query($queryParams);
        }

        error_log('🌐 Calling API: ' . $url);

        $response = $this->httpClient->request('GET', $url);
        return $response->toArray();
    }

    public function getAvgTrj(array $filters = []): array
    {
        $queryParams = [];

        if (!empty($filters['sport'])) {
            $queryParams['sport'] = $filters['sport'];
        }
        if (!empty($filters['bookmaker'])) {
            $queryParams['bookmaker'] = $filters['bookmaker'];
        }
        if (!empty($filters['league'])) {
            $queryParams['league'] = $filters['league'];
        }
        if (!empty($filters['match'])) {
            $queryParams['match'] = $filters['match'];
        }
        if (!empty($filters['start'])) {
            $queryParams['start'] = $filters['start'];
        }
        if (!empty($filters['end'])) {
            $queryParams['end'] = $filters['end'];
        }

        $url = $this->apiBaseUrl . '/avg-trj';
        if (!empty($queryParams)) {
            $url .= '?' . http_build_query($queryParams);
        }

        error_log('🌐 Calling API: ' . $url);

        $response = $this->httpClient->request('GET', $url);
        return $response->toArray();
    }

    public function getOddsWithEvolution(array $filters = []): array
    {
        try {
            $queryParams = [];

            if (!empty($filters['sport'])) {
                $queryParams['sport'] = $filters['sport'];
            }
            if (!empty($filters['bookmaker'])) {
                $queryParams['bookmaker'] = $filters['bookmaker'];
            }
            if (!empty($filters['league'])) {
                $queryParams['league'] = $filters['league'];
            }
            if (!empty($filters['match'])) {
                $queryParams['match'] = $filters['match'];
            }
            if (!empty($filters['start'])) {
                $queryParams['start'] = $filters['start'];
            }
            if (!empty($filters['end'])) {
                $queryParams['end'] = $filters['end'];
            }

            $url = $this->apiBaseUrl . '/odds-with-evolution';
            if (!empty($queryParams)) {
                $url .= '?' . http_build_query($queryParams);
            }

            error_log('🌐 Calling API (with evolution): ' . $url);

            $response = $this->httpClient->request('GET', $url);
            return $response->toArray();
        } catch (\Exception $e) {
            error_log('❌ API Error (getOddsWithEvolution): ' . $e->getMessage());
            return [];
        }
    }

    public function getAvgTrjWithEvolution(array $filters = []): array
    {
        try {
            $queryParams = [];

            if (!empty($filters['sport'])) {
                $queryParams['sport'] = $filters['sport'];
            }
            if (!empty($filters['bookmaker'])) {
                $queryParams['bookmaker'] = $filters['bookmaker'];
            }
            if (!empty($filters['league'])) {
                $queryParams['league'] = $filters['league'];
            }
            if (!empty($filters['match'])) {
                $queryParams['match'] = $filters['match'];
            }
            if (!empty($filters['start'])) {
                $queryParams['start'] = $filters['start'];
            }
            if (!empty($filters['end'])) {
                $queryParams['end'] = $filters['end'];
            }

            $url = $this->apiBaseUrl . '/avg-trj-with-evolution';
            if (!empty($queryParams)) {
                $url .= '?' . http_build_query($queryParams);
            }

            error_log('🌐 Calling API (avg trj with evolution): ' . $url);

            $response = $this->httpClient->request('GET', $url);
            return $response->toArray();
        } catch (\Exception $e) {
            error_log('❌ API Error (getAvgTrjWithEvolution): ' . $e->getMessage());
            return [];
        }
    }

    // src/Service/OddsApiService.php

    public function triggerScraping(string $scraper): array
    {
        try {
            $response = $this->httpClient->request('POST', $this->apiBaseUrl . '/scraping/trigger', [
                'json' => ['scraper' => $scraper]
            ]);

            return $response->toArray();
        } catch (\Exception $e) {
            error_log('❌ API Error (triggerScraping): ' . $e->getMessage());
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }

    public function scrapeAllFootball(): array
    {
        try {
            $response = $this->httpClient->request('POST', $this->apiBaseUrl . '/scraping/football/all');
            return $response->toArray();
        } catch (\Exception $e) {
            error_log('❌ API Error (scrapeAllFootball): ' . $e->getMessage());
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }
}
