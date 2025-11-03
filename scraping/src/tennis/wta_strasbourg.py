# scraping/src/tennis/wta_strasbourg.py

from ._scraper_utils import scrape_league


def scrape_wta_strasbourg():
    """Scrape WTA Strasbourg"""
    return scrape_league(
        league_name="WTA Strasbourg",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-strasbourg",
        display_name="WTA Strasbourg"
    )
