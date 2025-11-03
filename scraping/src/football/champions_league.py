# scraping/src/football/champions_league.py

from ._scraper_utils import scrape_league


def scrape_champions_league():
    """Scrape Champions League"""
    return scrape_league(
        league_name="Champions League",
        league_url="https://www.coteur.com/cotes/foot/europe/ligue-des-champions",
        display_name="Champions League"
    )
