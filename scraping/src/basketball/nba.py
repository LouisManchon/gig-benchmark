# scraping/src/basketball/nba.py

from ._scraper_utils import scrape_league


def scrape_nba():
    """Scrape NBA"""
    return scrape_league(
        league_name="NBA",
        league_url="https://www.coteur.com/cotes/basket/etats-unis/nba",
        display_name="NBA"
    )
