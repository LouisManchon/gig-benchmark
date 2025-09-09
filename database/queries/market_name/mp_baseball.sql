USE GIG;

INSERT INTO MarketNames (sport_id, code, name) VALUES
    ((SELECT id FROM Sports WHERE code='BASB'), '12', '12'),
    ((SELECT id FROM Sports WHERE code='BASB'), 'H2W',  'Handicap 2 way'),
    ((SELECT id FROM Sports WHERE code='BASB'), 'OU',   'Over / Under')
ON DUPLICATE KEY UPDATE name = VALUES(name);

SELECT * FROM MarketNames WHERE sport_id = (SELECT id FROM Sports WHERE code='BASB')
ORDER BY id;
