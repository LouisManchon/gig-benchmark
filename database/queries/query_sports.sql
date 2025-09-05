USE GIG;

INSERT INTO Sports (code, name) VALUES
    ('FOOT', 'Football'),
    ('TENNIS', 'Tennis'),
    ('BASK', 'Basketball'),
    ('RUGB', 'Rugby'),
    ('ICEH', 'Ice_Hockey'),
    ('BASB', 'Base_Ball'),
    ('BOXE', 'Boxing'),
    ('HAND', 'HandBall'),
    ('VOLL', 'VolleyBall'),
    ('AMEF', 'American_Football'),
    ('RUBL', 'Rugby_League'),
    ('BADM', 'Badminton'),
    ('MMA', 'M_M_A')
ON DUPLICATE KEY UPDATE name = VALUES(name);
SELECT * FROM Sports ORDER BY id;
