# scraping/src/football/erovnuli_liga.py

from ._scraper_utils import scrape_league


def scrape_erovnuli_liga():
    """Scrape Erovnuli Liga"""
    return scrape_league(
        league_name="Erovnuli Liga",
        league_url="https://www.coteur.com/cotes/foot/georgie/erovnuli-liga",
        display_name="Erovnuli Liga"
    )
