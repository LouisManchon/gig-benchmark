# scraping/src/tennis/wta_bad_homburg.py

from ._scraper_utils import scrape_league


def scrape_wta_bad_homburg():
    """Scrape WTA Bad Homburg"""
    return scrape_league(
        league_name="WTA Bad Homburg",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-bad-homburg",
        display_name="WTA Bad Homburg"
    )
