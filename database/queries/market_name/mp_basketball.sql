USE GIG;

INSERT INTO MarketNames (sport_id, code, name) VALUES
    ((SELECT id FROM Sports WHERE code='BASK'), '12', '12'),
    ((SELECT id FROM Sports WHERE code='BASK'), 'H2W', 'Handicap 2 way'),
    ((SELECT id FROM Sports WHERE code='BASK'), '1X2', '1X2')
ON DUPLICATE KEY UPDATE name = VALUES(name);

SELECT * FROM MarketNames WHERE sport_id = (SELECT id FROM Sports WHERE code='BASK')
ORDER BY id;
