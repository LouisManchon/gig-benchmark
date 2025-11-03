# scraping/src/tennis/wta_pekin.py

from ._scraper_utils import scrape_league


def scrape_wta_pekin():
    """Scrape WTA Pékin"""
    return scrape_league(
        league_name="WTA Pékin",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-pekin",
        display_name="WTA Pékin"
    )
