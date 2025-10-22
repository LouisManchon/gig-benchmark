SELECT * FROM odds;
SELECT DISTINCT DATE(created_at) as scraping_date, COUNT(*) as nb_odds
FROM odds
GROUP BY DATE(created_at)
ORDER BY scraping_date DESC
LIMIT 5;