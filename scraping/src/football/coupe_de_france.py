# scraping/src/football/coupe_de_france.py

from ._scraper_utils import scrape_league


def scrape_coupe_de_france():
    """Scrape Coupe de France"""
    return scrape_league(
        league_name="Coupe de France",
        league_url="https://www.coteur.com/cotes/foot/france/coupe-de-france",
        display_name="Coupe de France"
    )
