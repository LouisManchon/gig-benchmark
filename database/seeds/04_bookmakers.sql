-- Bookmakers from coteur.com
INSERT INTO Bookmakers (code, name, website) VALUES
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
  ('BET365', 'Bet365', 'https://www.bet365.com'),
  ('NETBET', 'NetBet', 'https://www.netbet.fr'),
  ('PINNACLE', 'Pinnacle', 'https://www.pinnacle.com'),
  ('POKERSTARS', 'Pokerstars Sport', 'https://www.pokerstars.fr')
ON DUPLICATE KEY UPDATE
  name = VALUES(name),
  website = VALUES(website);

SELECT 'Bookmakers OK!' as Status;
SELECT COUNT(*) as Total FROM Bookmakers;
