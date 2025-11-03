# scraping/src/basketball/coupe_d_europe_fiba.py

from ._scraper_utils import scrape_league


def scrape_coupe_d_europe_fiba():
    """Scrape Coupe d'Europe FIBA"""
    return scrape_league(
        league_name="Coupe d'Europe FIBA",
        league_url="https://www.coteur.com/cotes/basket/europe/coupe-deurope-fiba",
        display_name="Coupe d'Europe FIBA"
    )
