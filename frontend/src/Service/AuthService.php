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

            $data = json_decode($response->getContent(false), true);

            return [
                'success' => $response->getStatusCode() === 201,
                'data' => $data,
                'user' => $data['user'] ?? null,
                'tokens' => $data['tokens'] ?? null
            ];
        } catch (\Exception $e) {
            // Get error details from response
            $statusCode = method_exists($e, 'getResponse') ? $e->getResponse()->getStatusCode() : 500;
            $errorContent = method_exists($e, 'getResponse') ? $e->getResponse()->getContent(false) : '{}';
            $errorData = json_decode($errorContent, true);

            return [
                'success' => false,
                'error' => $e->getMessage(),
                'data' => $errorData ?? []
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
                'tokens' => $data['tokens'] ?? null,
                'user' => $data['user'] ?? null,
                'error' => $data['error'] ?? null
            ];
        } catch (\Exception $e) {
            return [
                'success' => false,
                'error' => $e->getMessage()
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