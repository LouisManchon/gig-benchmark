-- Shema (dev-version) - Adapté pour Django
-- GIG DB
CREATE DATABASE IF NOT EXISTS GIG
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_general_ci;
USE GIG;

-- =============================================
-- TABLES SYSTÈME DJANGO (requises)
-- =============================================
CREATE TABLE django_migrations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE django_session (
    session_key VARCHAR(40) NOT NULL PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE django_content_type (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE KEY django_content_type_app_label_model_76bd3d3b_uniq (app_label, model)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE auth_permission (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL,
    codename VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE auth_group (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE auth_group_permissions (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    group_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    UNIQUE KEY auth_group_permissions_group_id_permission_id_0cd325b0_uniq (group_id, permission_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE auth_user (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE auth_user_groups (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    UNIQUE KEY auth_user_groups_user_id_group_id_94350c0c_uniq (user_id, group_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE auth_user_user_permissions (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    UNIQUE KEY auth_user_user_permissions_user_id_permission_id_14a6b8e4_uniq (user_id, permission_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- VOS TABLES EXISTANTES (inchangées)
-- =============================================
CREATE TABLE Sports (
  id TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  code VARCHAR(20)  NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE MarketNames (
  id INT PRIMARY KEY AUTO_INCREMENT,
  sport_id TINYINT UNSIGNED NOT NULL,
  code VARCHAR(50)  NOT NULL,
  name VARCHAR(150) NOT NULL,
  UNIQUE KEY uniq_market_per_sport (sport_id, code),
  FOREIGN KEY (sport_id) REFERENCES Sports(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Leagues (
  id INT PRIMARY KEY AUTO_INCREMENT,
  sport_id TINYINT UNSIGNED NOT NULL,
  code VARCHAR(50)  NULL,
  name VARCHAR(150) NOT NULL,
  country VARCHAR(100) NULL,
  UNIQUE KEY uniq_league_per_sport (sport_id, name),
  FOREIGN KEY (sport_id) REFERENCES Sports(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Teams (
  id INT PRIMARY KEY AUTO_INCREMENT,
  league_id INT NOT NULL,
  name VARCHAR(150) NOT NULL,
  UNIQUE KEY uniq_team_per_league (league_id, name),
  KEY ix_team_league (league_id),
  FOREIGN KEY (league_id) REFERENCES Leagues(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Players (
  id INT PRIMARY KEY AUTO_INCREMENT,
  team_id INT NULL,
  full_name    VARCHAR(150) NOT NULL,
  nationality  VARCHAR(100) NULL,
  KEY ix_player_team (team_id),
  FOREIGN KEY (team_id) REFERENCES Teams(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
