-- Bookmakers from coteur.com
INSERT INTO Bookmakers (code, name, website, created_at, updated_at) VALUES
  ('PMU', 'PMU', 'https://www.pmu.fr', NOW(), NOW()),
  ('PARIONSSPORT', 'ParionsSport', 'https://www.parionssport.fdj.fr', NOW(), NOW()),
  ('ZEBET', 'ZEbet', 'https://www.zebet.fr', NOW(), NOW()),
  ('WINAMAX', 'Winamax', 'https://www.winamax.fr', NOW(), NOW()),
  ('BETCLIC', 'Betclic', 'https://www.betclic.fr', NOW(), NOW()),
  ('BETSSON', 'Betsson', 'https://www.betsson.fr', NOW(), NOW()),
  ('BWIN', 'Bwin', 'https://www.bwin.fr', NOW(), NOW()),
  ('UNIBET', 'Unibet', 'https://www.unibet.fr', NOW(), NOW()),
  ('OLYBET', 'OlyBet', 'https://www.olybet.fr', NOW(), NOW()),
  ('FEELINGBET', 'FeelingBet', 'https://www.feelingbet.fr', NOW(), NOW()),
  ('GENYBET', 'Genybet', 'https://www.genybet.fr', NOW(), NOW()),
  ('VBET', 'Vbet', 'https://www.vbet.fr', NOW(), NOW()),
  ('BET365', 'Bet365', 'https://www.bet365.com', NOW(), NOW()),
  ('NETBET', 'NetBet', 'https://www.netbet.fr', NOW(), NOW()),
  ('PINNACLE', 'Pinnacle', 'https://www.pinnacle.com', NOW(), NOW()),
  ('POKERSTARS', 'Pokerstars Sport', 'https://www.pokerstars.fr', NOW(), NOW())
ON DUPLICATE KEY UPDATE
  name = VALUES(name),
  website = VALUES(website),
  updated_at = NOW();

SELECT 'Bookmakers OK!' as Status;
SELECT COUNT(*) as Total FROM Bookmakers;
