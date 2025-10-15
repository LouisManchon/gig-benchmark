-- =============================================
-- Fichier: database/seeds/02_markets.sql
-- Description: Types de marchés de paris par sport
-- Usage: mysql -u root -p GIG < database/seeds/02_markets.sql
-- =============================================


-- =============================================
-- FOOTBALL - Marchés principaux
-- =============================================
INSERT INTO MarketNames (sport_id, code, name) VALUES
  ((SELECT id FROM Sports WHERE code='FOOT'), '1X2', '1X2 (Match Winner)'),
  ((SELECT id FROM Sports WHERE code='FOOT'), '1X2H1', '1X2 - 1st Half'),
  ((SELECT id FROM Sports WHERE code='FOOT'), '1X2H2', '1X2 - 2nd Half'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'BTTS', 'Both Teams To Score'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'DC', 'Double Chance'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'DNB', 'Draw No Bet'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'OU', 'Over/Under Goals'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'OU1H', 'Over/Under - 1st Half'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'FTS', 'First Team to Score'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'LTS', 'Last Team to Score'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'HC', 'Handicap'),
  ((SELECT id FROM Sports WHERE code='FOOT'), 'HTFT', 'Half Time / Full Time')
ON DUPLICATE KEY UPDATE 
  name = VALUES(name);

-- =============================================
-- BASKETBALL - Marchés principaux
-- =============================================
INSERT INTO MarketNames (sport_id, code, name) VALUES
  ((SELECT id FROM Sports WHERE code='BASK'), '1X2', 'Match Winner'),
  ((SELECT id FROM Sports WHERE code='BASK'), 'OU', 'Over/Under Points'),
  ((SELECT id FROM Sports WHERE code='BASK'), 'HC', 'Handicap'),
  ((SELECT id FROM Sports WHERE code='BASK'), 'OU1Q', 'Over/Under - 1st Quarter'),
  ((SELECT id FROM Sports WHERE code='BASK'), 'OU1H', 'Over/Under - 1st Half')
ON DUPLICATE KEY UPDATE 
  name = VALUES(name);

-- =============================================
-- TENNIS - Marchés principaux
-- =============================================
INSERT INTO MarketNames (sport_id, code, name) VALUES
  ((SELECT id FROM Sports WHERE code='TENN'), '1X2', 'Match Winner'),
  ((SELECT id FROM Sports WHERE code='TENN'), 'SET', 'Set Winner'),
  ((SELECT id FROM Sports WHERE code='TENN'), 'OU', 'Over/Under Games'),
  ((SELECT id FROM Sports WHERE code='TENN'), 'HC', 'Handicap Games')
ON DUPLICATE KEY UPDATE 
  name = VALUES(name);

-- =============================================
-- RUGBY - Marchés principaux
-- =============================================
INSERT INTO MarketNames (sport_id, code, name) VALUES
  ((SELECT id FROM Sports WHERE code='RUGB'), '1X2', '1X2 (Match Winner)'),
  ((SELECT id FROM Sports WHERE code='RUGB'), 'OU', 'Over/Under Points'),
  ((SELECT id FROM Sports WHERE code='RUGB'), 'HC', 'Handicap'),
  ((SELECT id FROM Sports WHERE code='RUGB'), 'OU1H', 'Over/Under - 1st Half')
ON DUPLICATE KEY UPDATE 
  name = VALUES(name);

-- Vérification
SELECT 'Markets inserted successfully!' as Status;
SELECT 
    s.name as Sport,
    COUNT(m.id) as Markets_Count
FROM Sports s
LEFT JOIN MarketNames m ON s.id = m.sport_id
GROUP BY s.name
ORDER BY s.name;