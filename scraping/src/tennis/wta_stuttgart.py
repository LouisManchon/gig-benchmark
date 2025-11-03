# scraping/src/tennis/wta_stuttgart.py

from ._scraper_utils import scrape_league


def scrape_wta_stuttgart():
    """Scrape WTA Stuttgart"""
    return scrape_league(
        league_name="WTA Stuttgart",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-stuttgart",
        display_name="WTA Stuttgart"
    )
