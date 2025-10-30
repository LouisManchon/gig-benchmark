<?php

namespace App\Service;

use Symfony\Contracts\HttpClient\HttpClientInterface;

class AuthService
{
    private HttpClientInterface $httpClient;
    private string $apiBaseUrl;

    public function __construct(HttpClientInterface $httpClient, string $apiBaseUrl
    ) {
        $this->apiBaseUrl = rtrim($apiBaseUrl, '/');
        $this->httpClient = $httpClient;
    }

    /**
     * Enregistre un nouvel utilisateur
     */
    public function register(array $userData): array
    {
        try {
            $response = $this->httpClient->request('POST', $this->apiBaseUrl . '/auth/register/', [
                'json' => $userData,
                'headers' => ['Content-Type' => 'application/json'],
            ]);

            return [
                'success' => $response->getStatusCode() === 201,
                'data' => json_decode($response->getContent(false), true)
            ];
        } catch (\Exception $e) {
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }

    /**
     * Connecte un utilisateur
     */
    public function login(string $username, string $password): array
    {
        try {
            $response = $this->httpClient->request('POST', $this->apiBaseUrl . '/auth/login/', [
                'json' => [
                    'username' => $username,
                    'password' => $password
                ],
                'headers' => ['Content-Type' => 'application/json'],
            ]);

            $data = json_decode($response->getContent(false), true);

            return [
                'success' => $response->getStatusCode() === 200,
                'token' => $data['access'] ?? null,
                'refresh' => $data['refresh'] ?? null,
                'user' => $data['user'] ?? null
            ];
        } catch (\Exception $e) {
            return [
                'success' => false,
                'error' => 'Identifiants invalides'
            ];
        }
    }

    /**
     * Vérifie si un token est valide
     */
    public function verifyToken(string $token): bool
    {
        try {
            $response = $this->httpClient->request('POST', $this->apiBaseUrl . '/auth/verify/', [
                'json' => ['token' => $token],
                'headers' => ['Content-Type' => 'application/json'],
            ]);

            return $response->getStatusCode() === 200;
        } catch (\Exception $e) {
            return false;
        }
    }

    /**
     * Rafraîchit le token
     */
    public function refreshToken(string $refreshToken): ?string
    {
        try {
            $response = $this->httpClient->request('POST', $this->apiBaseUrl . '/auth/refresh/', [
                'json' => ['refresh' => $refreshToken],
                'headers' => ['Content-Type' => 'application/json'],
            ]);

            $data = json_decode($response->getContent(false), true);
            return $data['access'] ?? null;
        } catch (\Exception $e) {
            return null;
        }
    }
}
