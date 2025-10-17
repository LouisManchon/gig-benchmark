-- ============================================
-- GIG BENCHMARK - SCHEMA DE BASE DE DONNÉES
-- ============================================

-- Table des sports (Football, Basketball, Tennis, Rugby)
CREATE TABLE IF NOT EXISTS Sports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) NOT NULL UNIQUE COMMENT 'FOOT, BASK, TENN, RUGB',
    name VARCHAR(50) NOT NULL UNIQUE COMMENT 'Football, Basketball, Tennis, Rugby',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table des types de marchés (1X2, OU, BTTS, HC...)
CREATE TABLE IF NOT EXISTS MarketNames (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sport_id INT NOT NULL,
    code VARCHAR(10) NOT NULL COMMENT '1X2, OU, BTTS, HC',
    name VARCHAR(100) NOT NULL COMMENT '1X2 (Match Winner), Over/Under',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sport_id) REFERENCES Sports(id) ON DELETE CASCADE,
    UNIQUE KEY unique_market (sport_id, code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table des ligues/compétitions
CREATE TABLE IF NOT EXISTS Leagues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sport_id INT NOT NULL,
    code VARCHAR(50) NOT NULL COMMENT 'LIGUE_1, PREMIER_LEAGUE, NBA',
    name VARCHAR(100) NOT NULL COMMENT 'Ligue 1, Premier League',
    country VARCHAR(50) COMMENT 'France, England, USA',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sport_id) REFERENCES Sports(id) ON DELETE CASCADE,
    UNIQUE KEY unique_league (sport_id, code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table des équipes
CREATE TABLE IF NOT EXISTS Teams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    league_id INT NOT NULL,
    name VARCHAR(100) NOT NULL COMMENT 'PSG, OM, Manchester United',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (league_id) REFERENCES Leagues(id) ON DELETE CASCADE,
    UNIQUE KEY unique_team (league_id, name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table des bookmakers
CREATE TABLE IF NOT EXISTS Bookmakers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE COMMENT 'BETCLIC, WINAMAX, PMU',
    name VARCHAR(100) NOT NULL UNIQUE COMMENT 'Betclic, Winamax',
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table des matchs
CREATE TABLE IF NOT EXISTS Matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    league_id INT NOT NULL,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    match_date DATETIME NOT NULL,
    status ENUM('scheduled', 'live', 'finished', 'postponed') DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (league_id) REFERENCES Leagues(id) ON DELETE CASCADE,
    FOREIGN KEY (home_team_id) REFERENCES Teams(id) ON DELETE CASCADE,
    FOREIGN KEY (away_team_id) REFERENCES Teams(id) ON DELETE CASCADE,
    CHECK (home_team_id != away_team_id),
    INDEX idx_match_date (match_date),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table des cotes (LA PLUS IMPORTANTE)
CREATE TABLE IF NOT EXISTS Odds (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    market_id INT NOT NULL COMMENT 'Type de marché (1X2, OU...)',
    bookmaker_id INT NOT NULL,
    outcome VARCHAR(10) NOT NULL COMMENT '1, X, 2',
    odd_value DECIMAL(10, 2) NOT NULL COMMENT 'Valeur de la cote (1.85, 3.40)',
    trj DECIMAL(5, 2) NOT NULL COMMENT 'Taux de Retour Joueur en % (91.5)',
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES Matches(id) ON DELETE CASCADE,
    FOREIGN KEY (market_id) REFERENCES MarketNames(id) ON DELETE CASCADE,
    FOREIGN KEY (bookmaker_id) REFERENCES Bookmakers(id) ON DELETE CASCADE,
    INDEX idx_match (match_id),
    INDEX idx_bookmaker (bookmaker_id),
    INDEX idx_scraped (scraped_at),
    INDEX idx_outcome (outcome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
