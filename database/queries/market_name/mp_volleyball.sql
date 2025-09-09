USE GIG;

INSERT INTO MarketNames (sport_id, code, name) VALUES
    ((SELECT id FROM Sports WHERE code='VOLL'), '12', '12'),
    ((SELECT id FROM Sports WHERE code='VOLL'), 'H2W',  'Handicap 2 way'),
    ((SELECT id FROM Sports WHERE code='VOLL'), 'OUP',   'Over / Under Points')
ON DUPLICATE KEY UPDATE name = VALUES(name);

SELECT * FROM MarketNames WHERE sport_id = (SELECT id FROM Sports WHERE code='VOLL')
ORDER BY id;
