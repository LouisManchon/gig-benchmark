USE GIG;

INSERT INTO MarketNames (sport_id, code, name) VALUES
    ((SELECT id FROM Sports WHERE code='RUBL'), '1X2', '1X2'),
    ((SELECT id FROM Sports WHERE code='RUBL'), 'H2W',  'Handicap 2 way'),
    ((SELECT id FROM Sports WHERE code='RUBL'), 'OU',   'Over / Under')
ON DUPLICATE KEY UPDATE name = VALUES(name);

SELECT * FROM MarketNames WHERE sport_id = (SELECT id FROM Sports WHERE code='RUBL')
ORDER BY id;
