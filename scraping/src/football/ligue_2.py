# scraping/src/football/ligue_2.py

from ._scraper_utils import scrape_league


def scrape_ligue_2():
    """Scrape Ligue 2"""
    return scrape_league(
        league_name="Ligue 2",
        league_url="https://www.coteur.com/cotes/foot/france/ligue-2",
        display_name="Ligue 2"
    )
