-- =============================================
-- File: database/seeds/04_bookmakers.sql
-- Description: Complete bookmakers list from coteur.com (TRJ is scraped per match)
-- Usage: mysql -u root -p GIG < database/seeds/04_bookmakers.sql
-- =============================================


-- Complete bookmakers list from coteur.com
INSERT INTO Bookmakers (code, name, website) VALUES
  -- Main French bookmakers
  ('PMU', 'PMU', 'https://www.pmu.fr'),
  ('PARIONSSPORT', 'ParionsSport', 'https://www.parionssport.fdj.fr'),
  ('ZEBET', 'ZEbet', 'https://www.zebet.fr'),
  ('WINAMAX', 'Winamax', 'https://www.winamax.fr'),
  ('BETCLIC', 'Betclic', 'https://www.betclic.fr'),
  ('BETSSON', 'Betsson', 'https://www.betsson.fr'),
  ('BWIN', 'Bwin', 'https://www.bwin.fr'),
  ('UNIBET', 'Unibet', 'https://www.unibet.fr'),
  ('OLYBET', 'OlyBet', 'https://www.olybet.fr'),
  ('FEELINGBET', 'FeelingBet', 'https://www.feelingbet.fr'),
  ('GENYBET', 'Genybet', 'https://www.genybet.fr'),
  ('VBET', 'Vbet', 'https://www.vbet.fr'),
  ('POKERSTARS', 'Pokerstars Sport', 'https://www.pokerstars.fr')
  
  -- Additional international bookmakers
  ('BET365', 'Bet365', 'https://www.bet365.com'),
  ('NETBET', 'NetBet', 'https://www.netbet.fr'),
  ('PINNACLE', 'Pinnacle', 'https://www.pinnacle.com')
ON DUPLICATE KEY UPDATE 
  name = VALUES(name),
  website = VALUES(website);

-- Verification
SELECT 'Bookmakers inserted successfully!' as Status;
SELECT 
    code,
    name,
    website
FROM Bookmakers
ORDER BY name;