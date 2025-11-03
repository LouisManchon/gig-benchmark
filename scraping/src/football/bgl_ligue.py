# scraping/src/football/bgl_ligue.py

from ._scraper_utils import scrape_league


def scrape_bgl_ligue():
    """Scrape BGL Ligue"""
    return scrape_league(
        league_name="BGL Ligue",
        league_url="https://www.coteur.com/cotes/foot/luxembourg/bgl-ligue",
        display_name="BGL Ligue"
    )
