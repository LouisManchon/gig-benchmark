from src.football.ligue_1 import scrape_ligue_1
from src.football.premier_league import scrape_premier_league
from src.football.la_liga import scrape_la_liga
from src.football.serie_a import scrape_serie_a
from src.football.bundesliga import scrape_bundesliga
from src.football.champion_league import scrape_champion_league

from src.basketball.nba import scrape_nba
from src.basketball.euro_league import scrape_euro_league

from src.rugby.top_14 import scrape_top_14

from src.tennis.atp import scrape_atp
from src.tennis.wta import scrape_wta

# Registre des scrapers disponibles
SCRAPERS_REGISTRY: Dict[str, Callable] = {
    # Football
    'football.ligue_1': scrape_ligue_1,
    'football.premier_league': scrape_premier_league,
    'football.la_liga': scrape_la_liga,
    'football.serie_a': scrape_serie_a,
    'football.bundesliga': scrape_bundesliga,
    'football.champions_league': scrape_champion_league,
   
    # Basketball
    'basketball.nba': scrape_nba,
    'basketball.euroleague': scrape_euro_league,
  
    # Rugby
    'rugby.top14': scrape_top_14,
 
    # Tennis
    'tennis.atp': scrape_atp,
    'tennis.wta': scrape_wta,
}