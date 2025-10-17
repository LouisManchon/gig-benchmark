<?php

// src/Service/OddsApiService.php
namespace App\Service;

use Symfony\Contracts\HttpClient\HttpClientInterface;

class OddsApiService
{
    private $httpClient;
    private $apiBaseUrl;

    public function __construct(HttpClientInterface $httpClient, string $apiBaseUrl = 'http://backend:8000/api/scraping/')
    {
        $this->httpClient = $httpClient;
        $this->apiBaseUrl = $apiBaseUrl;
    }

    public function healthCheck(): array
    {
        $response = $this->httpClient->request('GET', $this->apiBaseUrl . 'health');
        return $response->toArray();
    }

    public function listScrapers(): array
    {
        $response = $this->httpClient->request('GET', $this->apiBaseUrl . 'scrapers');
        return $response->toArray();
    }

    public function triggerScraping(array $data): array
    {
        $response = $this->httpClient->request('POST', $this->apiBaseUrl . 'trigger', [
            'json' => $data,
        ]);
        return $response->toArray();
    }
}

