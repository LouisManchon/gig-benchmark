-- =============================================
-- Fichier: database/seeds/03_leagues.sql
-- Description: Ligues et compétitions par sport
-- Usage: mysql -u root -p GIG < database/seeds/03_leagues.sql
-- =============================================


-- =============================================
-- FOOTBALL - Ligues principales
-- =============================================
INSERT INTO Leagues (sport_id, code, name, country) VALUES
  -- France
  ((SELECT id FROM Sports WHERE code='FOOT'), 'LIGUE_1', 'Ligue 1', 'France'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'LIGUE_2', 'Ligue 2', 'France'),
  
  -- Angleterre
  ((SELECT id FROM Sports WHERE code='FOOT'), 'PREMIER_LEAGUE', 'Premier League', 'England'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'CHAMPIONSHIP', 'Championship', 'England'),
  
  -- Espagne
  ((SELECT id FROM Sports WHERE code='FOOT'), 'LA_LIGA', 'La Liga', 'Spain'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'SEGUNDA', 'Segunda División', 'Spain'),
  
  -- Italie
  ((SELECT id FROM Sports WHERE code='FOOT'), 'SERIE_A', 'Serie A', 'Italy'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'SERIE_B', 'Serie B', 'Italy'),
  
  -- Allemagne
  ((SELECT id FROM Sports WHERE code='FOOT'), 'BUNDESLIGA', 'Bundesliga', 'Germany'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'BUNDESLIGA_2', '2. Bundesliga', 'Germany'),
  
  -- Compétitions européennes
  ((SELECT id FROM Sports WHERE code='FOOT'), 'UCL', 'UEFA Champions League', 'Europe'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'UEL', 'UEFA Europa League', 'Europe'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'UECL', 'UEFA Conference League', 'Europe')
ON DUPLICATE KEY UPDATE 
  name = VALUES(name),
  country = VALUES(country);

-- =============================================
-- BASKETBALL - Ligues principales
-- =============================================
INSERT INTO Leagues (sport_id, code, name, country) VALUES
  ((SELECT id FROM Sports WHERE code='BASK'), 'NBA', 'NBA', 'USA'),
  ((SELECT id FROM Sports WHERE code='BASK'), 'EUROLEAGUE', 'EuroLeague', 'Europe'),
  ((SELECT id FROM Sports WHERE code='BASK'), 'LNB', 'LNB Pro A', 'France')
ON DUPLICATE KEY UPDATE 
  name = VALUES(name),
  country = VALUES(country);

-- =============================================
-- TENNIS - Tournois principaux
-- =============================================
INSERT INTO Leagues (sport_id, code, name, country) VALUES
  ((SELECT id FROM Sports WHERE code='TENN'), 'ATP', 'ATP Tour', 'International'),
  ((SELECT id FROM Sports WHERE code='TENN'), 'WTA', 'WTA Tour', 'International'),
  ((SELECT id FROM Sports WHERE code='TENN'), 'GRAND_SLAM', 'Grand Slam', 'International')
ON DUPLICATE KEY UPDATE 
  name = VALUES(name),
  country = VALUES(country);

-- =============================================
-- RUGBY - Ligues principales
-- =============================================
INSERT INTO Leagues (sport_id, code, name, country) VALUES
  ((SELECT id FROM Sports WHERE code='RUGB'), 'TOP14', 'Top 14', 'France'),
  ((SELECT id FROM Sports WHERE code='RUGB'), 'PRO_D2', 'Pro D2', 'France'),
  ((SELECT id FROM Sports WHERE code='RUGB'), 'PREMIERSHIP', 'Premiership Rugby', 'England'),
  ((SELECT id FROM Sports WHERE code='RUGB'), 'URC', 'United Rugby Championship', 'Europe')
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