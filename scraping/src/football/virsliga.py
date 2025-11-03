# scraping/src/football/virsliga.py

from ._scraper_utils import scrape_league


def scrape_virsliga():
    """Scrape Virsliga"""
    return scrape_league(
        league_name="Virsliga",
        league_url="https://www.coteur.com/cotes/foot/lettonie/virsliga",
        display_name="Virsliga"
    )
