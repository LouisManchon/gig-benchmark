# scraping/src/football/fa_cup.py

from ._scraper_utils import scrape_league


def scrape_fa_cup():
    """Scrape FA Cup"""
    return scrape_league(
        league_name="FA Cup",
        league_url="https://www.coteur.com/cotes/foot/angleterre/fa-cup",
        display_name="FA Cup"
    )
