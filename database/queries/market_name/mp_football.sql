USE GIG;

INSERT INTO MarketNames (sport_id, code, name) VALUES
    ((SELECT id FROM Sports WHERE code='FOOT'), '1X2', '1X2'),
    ((SELECT id FROM Sports WHERE code='FOOT'), '1X2H1', '1X2 - 1st Half'),
    ((SELECT id FROM Sports WHERE code='FOOT'), '1X2H2', '1X2 - 2nd Half'),
    ((SELECT id FROM Sports WHERE code='FOOT'), 'BTTS', 'Both Teams To Score'),
    ((SELECT id FROM Sports WHERE code='FOOT'), 'DC',   'Double chance'),
    ((SELECT id FROM Sports WHERE code='FOOT'), 'DCH1', 'Double chance - 1st Half'),
    ((SELECT id FROM Sports WHERE code='FOOT'), 'DNB',  'Draw No Bet'),
    ((SELECT id FROM Sports WHERE code='FOOT'), 'FTS',  'First team to score'),
    ((SELECT id FROM Sports WHERE code='FOOT'), 'LTS',  'Last team to score'),
    ((SELECT id FROM Sports WHERE code='FOOT'), 'H2W',  'Handicap 2 way'),
    ((SELECT id FROM Sports WHERE code='FOOT'), 'H3W',  'Handicap 3 way'),
    ((SELECT id FROM Sports WHERE code='FOOT'), 'HTFT', 'HT/FT'),
    ((SELECT id FROM Sports WHERE code='FOOT'), 'OU',   'Over / Under'),
    ((SELECT id FROM Sports WHERE code='FOOT'), 'OUH1', 'Over / Under - 1st Half'),
    ((SELECT id FROM Sports WHERE code='FOOT'), 'OUG',  'Over / Under games'),
    ((SELECT id FROM Sports WHERE code='FOOT'), 'OUP',  'Over / Under points')
ON DUPLICATE KEY UPDATE name = VALUES(name);

SELECT * FROM MarketNames WHERE sport_id = (SELECT id FROM Sports WHERE code='FOOT')
ORDER BY id;
