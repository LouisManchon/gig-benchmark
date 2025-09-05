USE GIG;

INSERT INTO MarketNames (sport_id, code, name) VALUES
    ((SELECT id FROM Sports WHERE code='MMA'), 'Draw no bet', '12')

ON DUPLICATE KEY UPDATE name = VALUES(name);

SELECT * FROM MarketNames WHERE sport_id = (SELECT id FROM Sports WHERE code='MMA')
ORDER BY id;
