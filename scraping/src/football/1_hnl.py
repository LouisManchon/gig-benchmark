# scraping/src/football/1_hnl.py

from ._scraper_utils import scrape_league


def scrape_1_hnl():
    """Scrape 1.HNL"""
    return scrape_league(
        league_name="1.HNL",
        league_url="https://www.coteur.com/cotes/foot/croatie/1-hnl",
        display_name="1.HNL"
    )
