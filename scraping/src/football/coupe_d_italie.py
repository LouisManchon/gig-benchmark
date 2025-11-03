# scraping/src/football/coupe_d_italie.py

from ._scraper_utils import scrape_league


def scrape_coupe_d_italie():
    """Scrape Coupe d'Italie"""
    return scrape_league(
        league_name="Coupe d'Italie",
        league_url="https://www.coteur.com/cotes/foot/italie/coupe-ditalie",
        display_name="Coupe d'Italie"
    )
