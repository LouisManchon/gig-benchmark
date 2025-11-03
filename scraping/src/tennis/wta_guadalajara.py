# scraping/src/tennis/wta_guadalajara.py

from ._scraper_utils import scrape_league


def scrape_wta_guadalajara():
    """Scrape WTA Guadalajara"""
    return scrape_league(
        league_name="WTA Guadalajara",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-guadalajara",
        display_name="WTA Guadalajara"
    )
