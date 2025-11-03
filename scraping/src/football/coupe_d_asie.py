# scraping/src/football/coupe_d_asie.py

from ._scraper_utils import scrape_league


def scrape_coupe_d_asie():
    """Scrape Coupe d'Asie"""
    return scrape_league(
        league_name="Coupe d'Asie",
        league_url="https://www.coteur.com/cotes/foot/asie/coupe-dasie-des-nations",
        display_name="Coupe d'Asie"
    )
