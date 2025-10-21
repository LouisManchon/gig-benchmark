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
        // ✅ S'assurer que l'URL se termine par /api
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

        // ✅ Debug
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

            // ✅ Debug
        error_log('🌐 Calling API: ' . $url);

        $response = $this->httpClient->request('GET', $url);
        return $response->toArray();
    }
}
