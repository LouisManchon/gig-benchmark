# scraping/src/football/hnl_1.py

from ._scraper_utils import scrape_league


def scrape_hnl_1():
    """Scrape Division 1  Chypre"""
    return scrape_league(
        league_name="HNL 1",
        league_url="https://www.coteur.com/cotes/foot/croatie/1-hnl",
        display_name="HNL 1"
    )
