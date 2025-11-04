<?php
require __DIR__ . '/vendor/autoload.php';

use Symfony\Component\Dotenv\Dotenv;

$dotenv = new Dotenv();
$dotenv->loadEnv(__DIR__ . '/.env');

echo "BACKEND_API_URL from .env: " . ($_ENV['BACKEND_API_URL'] ?? 'NOT SET') . PHP_EOL;
echo "BACKEND_API_URL from getenv: " . (getenv('BACKEND_API_URL') ?: 'NOT SET') . PHP_EOL;

// Test what AuthService would use
$apiBaseUrl = $_ENV['BACKEND_API_URL'] ?? 'NOT FOUND';
$apiBaseUrl = rtrim($apiBaseUrl, '/');
echo "After rtrim: " . $apiBaseUrl . PHP_EOL;
echo "Login URL would be: " . $apiBaseUrl . '/auth/login/' . PHP_EOL;
