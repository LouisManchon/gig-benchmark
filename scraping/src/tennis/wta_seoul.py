# scraping/src/tennis/wta_seoul.py

from ._scraper_utils import scrape_league


def scrape_wta_seoul():
    """Scrape WTA Séoul"""
    return scrape_league(
        league_name="WTA Séoul",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-seoul",
        display_name="WTA Séoul"
    )
