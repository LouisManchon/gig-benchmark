# scraping/src/football/meistriliiga.py

from ._scraper_utils import scrape_league


def scrape_meistriliiga():
    """Scrape Meistriliiga"""
    return scrape_league(
        league_name="Meistriliiga",
        league_url="https://www.coteur.com/cotes/foot/estonie/meistriliiga",
        display_name="Meistriliiga"
    )
