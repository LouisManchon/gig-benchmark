-- Shema (dev-version/!\rootprivilege/!\)

-- GIG DB

CREATE DATABASE IF NOT EXISTS GIG
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_general_ci;
USE GIG;

-- ROOT TABLES

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
  UNIQUE KEY uniq_market_per_sport (sport_id, code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Arbo leagues -> teams -> players

CREATE TABLE Leagues (
  id INT PRIMARY KEY AUTO_INCREMENT,
  sport_id TINYINT UNSIGNED NOT NULL,
  code VARCHAR(50)  NULL,              
  name VARCHAR(150) NOT NULL,
  country VARCHAR(100) NULL,
  UNIQUE KEY uniq_league_per_sport (sport_id, name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Teams (
  id INT PRIMARY KEY AUTO_INCREMENT,
  league_id INT NOT NULL,             
  name VARCHAR(150) NOT NULL,
  UNIQUE KEY uniq_team_per_league (league_id, name),
  KEY ix_team_league (league_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Players (
  id INT PRIMARY KEY AUTO_INCREMENT,
  team_id INT NULL,
  full_name    VARCHAR(150) NOT NULL,
  nationality  VARCHAR(100) NULL,
  KEY ix_player_team (team_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
