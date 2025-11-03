-- =============================================
-- Fichier: database/seeds/03_leagues.sql
-- Description: Ligues et compétitions par sport
-- Usage: mysql -u root -p GIG < database/seeds/03_leagues.sql
-- =============================================


-- =============================================
-- FOOTBALL - Ligues principales
-- =============================================
INSERT INTO Leagues (sport_id, code, name, country, created_at, updated_at) VALUES
  -- France
  ((SELECT id FROM Sports WHERE code='FOOT'), 'LIGUE_1', 'Ligue 1', 'France', NOW(), NOW()),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'LIGUE_2', 'Ligue 2', 'France', NOW(), NOW()),
  
  -- Angleterre
  ((SELECT id FROM Sports WHERE code='FOOT'), 'PREMIER_LEAGUE', 'Premier League', 'England', NOW(), NOW()),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'CHAMPIONSHIP', 'Championship', 'England', NOW(), NOW()),
  
  -- Espagne
  ((SELECT id FROM Sports WHERE code='FOOT'), 'LA_LIGA', 'La Liga', 'Spain', NOW(), NOW()),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'SEGUNDA', 'Segunda División', 'Spain', NOW(), NOW()),
  
  -- Italie
  ((SELECT id FROM Sports WHERE code='FOOT'), 'SERIE_A', 'Serie A', 'Italy', NOW(), NOW()),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'SERIE_B', 'Serie B', 'Italy', NOW(), NOW()),
  
  -- Allemagne
  ((SELECT id FROM Sports WHERE code='FOOT'), 'BUNDESLIGA', 'Bundesliga', 'Germany', NOW(), NOW()),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'BUNDESLIGA_2', '2. Bundesliga', 'Germany', NOW(), NOW()),
  
  -- Compétitions européennes
  ((SELECT id FROM Sports WHERE code='FOOT'), 'UCL', 'UEFA Champions League', 'Europe', NOW(), NOW()),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'UEL', 'UEFA Europa League', 'Europe', NOW(), NOW()),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'UECL', 'UEFA Conference League', 'Europe', NOW(), NOW())
ON DUPLICATE KEY UPDATE 
  name = VALUES(name),
  country = VALUES(country);

-- =============================================
-- BASKETBALL - Ligues principales
-- =============================================
INSERT INTO Leagues (sport_id, code, name, country, created_at, updated_at) VALUES
  ((SELECT id FROM Sports WHERE code='BASK'), 'NBA', 'NBA', 'USA', NOW(), NOW()),
  ((SELECT id FROM Sports WHERE code='BASK'), 'EUROLEAGUE', 'EuroLeague', 'Europe', NOW(), NOW()),
  ((SELECT id FROM Sports WHERE code='BASK'), 'LNB', 'LNB Pro A', 'France', NOW(), NOW())
ON DUPLICATE KEY UPDATE 
  name = VALUES(name),
  country = VALUES(country);

-- =============================================
-- TENNIS - Tournois principaux
-- =============================================
INSERT INTO Leagues (sport_id, code, name, country, created_at, updated_at) VALUES
  ((SELECT id FROM Sports WHERE code='TENN'), 'ATP', 'ATP Tour', 'International', NOW(), NOW()),
  ((SELECT id FROM Sports WHERE code='TENN'), 'WTA', 'WTA Tour', 'International', NOW(), NOW()),
  ((SELECT id FROM Sports WHERE code='TENN'), 'GRAND_SLAM', 'Grand Slam', 'International', NOW(), NOW())
ON DUPLICATE KEY UPDATE 
  name = VALUES(name),
  country = VALUES(country);

-- =============================================
-- RUGBY - Ligues principales
-- =============================================
INSERT INTO Leagues (sport_id, code, name, country, created_at, updated_at) VALUES
  ((SELECT id FROM Sports WHERE code='RUGB'), 'TOP14', 'Top 14', 'France', NOW(), NOW()),
  ((SELECT id FROM Sports WHERE code='RUGB'), 'PRO_D2', 'Pro D2', 'France', NOW(), NOW()),
  ((SELECT id FROM Sports WHERE code='RUGB'), 'PREMIERSHIP', 'Premiership Rugby', 'England', NOW(), NOW()),
  ((SELECT id FROM Sports WHERE code='RUGB'), 'URC', 'United Rugby Championship', 'Europe', NOW(), NOW())
ON DUPLICATE KEY UPDATE 
  name = VALUES(name),
  country = VALUES(country);

-- Vérification
SELECT 'Leagues inserted successfully!' as Status;
SELECT 
    s.name as Sport,
    COUNT(l.id) as Leagues_Count
FROM Sports s
LEFT JOIN Leagues l ON s.id = l.sport_id
GROUP BY s.name
ORDER BY s.name;