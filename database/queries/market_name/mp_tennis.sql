USE GIG;

INSERT INTO MarketNames (sport_id, code, name) VALUES
    ((SELECT id FROM Sports WHERE code='TENNIS'), '12', '12'),
    ((SELECT id FROM Sports WHERE code='TENNIS'), '12S1', '1X2 - 1st Set'),
    ((SELECT id FROM Sports WHERE code='TENNIS'), '12S2', '1X2 - 2nd Set'),
    ((SELECT id FROM Sports WHERE code='TENNIS'), 'H2W',  'Handicap 2 way'),
    ((SELECT id FROM Sports WHERE code='TENNIS'), 'OU',   'Over / Under'),
    ((SELECT id FROM Sports WHERE code='TENNIS'), 'OUH1', 'Over / Under - 1st Half'),
    ((SELECT id FROM Sports WHERE code='TENNIS'), 'BPWS', 'Both Player win set')
ON DUPLICATE KEY UPDATE name = VALUES(name);

SELECT * FROM MarketNames WHERE sport_id = (SELECT id FROM Sports WHERE code='TENNIS')
ORDER BY id;
