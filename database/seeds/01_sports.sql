-- =============================================
-- Fichier: database/seeds/01_sports.sql
-- Description: Données de référence des sports
-- Usage: mysql -u root -p GIG < database/seeds/01_sports.sql
-- =============================================


-- Sports disponibles dans l'application
INSERT INTO Sports (code, name) VALUES
  ('FOOT', 'Football'),
  ('BASK', 'Basketball'),
  ('TENN', 'Tennis'),
  ('RUGB', 'Rugby')
ON DUPLICATE KEY UPDATE 
  name = VALUES(name);

-- Vérification
SELECT 'Sports inserted successfully!' as Status;
SELECT * FROM Sports ORDER BY name;