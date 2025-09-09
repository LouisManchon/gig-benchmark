USE GIG;

INSERT INTO MarketNames (sport_id, code, name) VALUES
    ((SELECT id FROM Sports WHERE code='AMEF'), '12', '12'),   
    ((SELECT id FROM Sports WHERE code='AMEF'), '1X2', '1X2'),
    ((SELECT id FROM Sports WHERE code='AMEF'), 'H2W',  'Handicap 2 way'),
    ((SELECT id FROM Sports WHERE code='AMEF'), 'OU',   'Over / Under')
ON DUPLICATE KEY UPDATE name = VALUES(name);

SELECT * FROM MarketNames WHERE sport_id = (SELECT id FROM Sports WHERE code='AMEF')
ORDER BY id;
