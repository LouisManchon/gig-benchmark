# scraping/src/basketball/betclic_elite.py

from ._scraper_utils import scrape_league


def scrape_betclic_elite():
    """Scrape Betclic Elite"""
    return scrape_league(
        league_name="Betclic Elite",
        league_url="https://www.coteur.com/cotes/basket/france/pro-a",
        display_name="Betclic Elite"
    )
