# scraping/src/football/veikkausliiga.py

from ._scraper_utils import scrape_league


def scrape_veikkausliiga():
    """Scrape Veikkausliiga"""
    return scrape_league(
        league_name="Veikkausliiga",
        league_url="https://www.coteur.com/cotes/foot/finlande/veikkausliiga",
        display_name="Veikkausliiga"
    )
