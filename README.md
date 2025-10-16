# 🎨 Frontend Symfony

Ce dépôt contient la partie **frontend** du projet, développée avec le framework **Symfony**.  
Il gère l’affichage, les routes publiques, et la communication avec l’API backend.

---

## 🚀 Prérequis

Avant de lancer le projet, assure-toi d’avoir installé :

- [PHP >= 8.3](https://www.php.net/downloads.php)

```bash
sudo apt update
sudo apt install php php-cli php-xml php-mbstring php-intl php-curl php-zip unzip git -y
sudo apt install composer -y
````
- [Symfony CLI](https://symfony.com/download)

```bash
wget https://get.symfony.com/cli/installer -O - | bash
sudo mv ~/.symfony*/bin/symfony /usr/local/bin/symfony
```

- Doctrine (si on veut lier la base de données directement dans Symfony)
```bash
composer require symfony/orm-pack
composer require symfony/doctrine-fixtures --dev
```

---

## ⚙️ Installation du projet

Clone le dépôt et installe les dépendances PHP et JS :

```bash
git clone [https://github.com/gig-benchmark.git](https://github.com/LouisManchon/gig-benchmark/tree/dorine/front)

# Installation des dépendances PHP
composer install

# Installation des dépendances frontend
npm install

```

## 🧑‍💻 Lancer le serveur de développement

Démarre le serveur Symfony :

``` bash
symfony serve
```

Par défaut, le site est accessible sur http://localhost:8000

## Structure du projet 

```bash
.
├── assets/              # Code JS/CSS source
├── config/              # Configuration Symfony
├── public/              # Fichiers publics (build, index.php, images, etc.)
├── src/                 # Code PHP (contrôleurs, services, etc.)
├── templates/           # Vues Twig
├── translations/        # Fichiers de traduction
├── .env                 # Configuration d'environnement
└── webpack.config.js    # Configuration Webpack Encore

```

