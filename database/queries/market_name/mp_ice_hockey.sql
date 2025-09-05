USE GIG;

INSERT INTO MarketNames (sport_id, code, name) VALUES
    ((SELECT id FROM Sports WHERE code='ICEH'), '1X2', '1X2'),
    ((SELECT id FROM Sports WHERE code='ICEH'), 'BTTS',  'Both Teams To Score'),
    ((SELECT id FROM Sports WHERE code='ICEH'), 'H2W',  'Handicap 2 way'),
    ((SELECT id FROM Sports WHERE code='ICEH'), 'H3W',  'Handicap 3 way'),
    ((SELECT id FROM Sports WHERE code='ICEH'), 'OU',   'Over / Under')
ON DUPLICATE KEY UPDATE name = VALUES(name);

SELECT * FROM MarketNames WHERE sport_id = (SELECT id FROM Sports WHERE code='ICEH')
ORDER BY id;
