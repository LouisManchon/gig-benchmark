# scraping/src/football/division_1_chypre.py

from ._scraper_utils import scrape_league


def scrape_division_1_chypre():
    """Scrape Division 1  Chypre"""
    return scrape_league(
        league_name="Division 1 Chypre",
        league_url="https://www.coteur.com/cotes/foot/chypre/1ere-division",
        display_name="Division 1 Chypre"
    )
