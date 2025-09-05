USE GIG;

INSERT INTO MarketNames (sport_id, code, name) VALUES
    ((SELECT id FROM Sports WHERE code='RUGB'), '1X2', '1X2'),
    ((SELECT id FROM Sports WHERE code='RUGB'), '1X2H1', '1X2 - 1st Half'),
    ((SELECT id FROM Sports WHERE code='RUGB'), '1X2H2', '1X2 - 2nd Half'),
    ((SELECT id FROM Sports WHERE code='RUGB'), 'DC',   'Double chance'),
    ((SELECT id FROM Sports WHERE code='RUGB'), 'DCH1', 'Double chance - 1st Half'),
    ((SELECT id FROM Sports WHERE code='RUGB'), 'DNB',  'Draw No Bet'),
    ((SELECT id FROM Sports WHERE code='RUGB'), 'H2W',  'Handicap 2 way'),
    ((SELECT id FROM Sports WHERE code='RUGB'), 'H3W',  'Handicap 3 way'),
    ((SELECT id FROM Sports WHERE code='RUGB'), 'OU',   'Over / Under'),
    ((SELECT id FROM Sports WHERE code='RUGB'), 'OUH1', 'Over / Under - 1st Half')
ON DUPLICATE KEY UPDATE name = VALUES(name);

SELECT * FROM MarketNames WHERE sport_id = (SELECT id FROM Sports WHERE code='RUGB')
ORDER BY id;
