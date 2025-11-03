# scraping/src/tennis/wta_osaka.py

from ._scraper_utils import scrape_league


def scrape_wta_osaka():
    """Scrape WTA Osaka"""
    return scrape_league(
        league_name="WTA Osaka",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-osaka",
        display_name="WTA Osaka"
    )
