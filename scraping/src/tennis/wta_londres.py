# scraping/src/tennis/wta_londres.py

from ._scraper_utils import scrape_league


def scrape_wta_londres():
    """Scrape WTA Londres"""
    return scrape_league(
        league_name="WTA Londres",
        league_url="https://www.coteur.com/cotes/tennis/monde-1/wta-londres",
        display_name="WTA Londres"
    )
