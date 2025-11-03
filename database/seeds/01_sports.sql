-- =============================================
-- Fichier: database/seeds/01_sports.sql
-- Description: Données de référence des sports
-- Usage: mysql -u root -p GIG < database/seeds/01_sports.sql
-- =============================================


-- Sports disponibles dans l'application
INSERT INTO Sports (code, name, created_at, updated_at) VALUES
  ('FOOT', 'Football', NOW(), NOW()),
  ('BASK', 'Basketball', NOW(), NOW()),
  ('TENN', 'Tennis', NOW(), NOW()),
  ('RUGB', 'Rugby', NOW(), NOW())
ON DUPLICATE KEY UPDATE
  name = VALUES(name),
  updated_at = NOW();

-- Vérification
SELECT 'Sports inserted successfully!' as Status;
SELECT * FROM Sports ORDER BY name;