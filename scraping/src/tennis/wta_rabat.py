# scraping/src/tennis/wta_rabat.py

from ._scraper_utils import scrape_league


def scrape_wta_rabat():
    """Scrape WTA Rabat"""
    return scrape_league(
        league_name="WTA Rabat",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-rabat",
        display_name="WTA Rabat"
    )
