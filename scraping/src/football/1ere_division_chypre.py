# scraping/src/football/1ere_division_chypre.py

from ._scraper_utils import scrape_league


def scrape_1ere_division_chypre():
    """Scrape 1ère division Chypre"""
    return scrape_league(
        league_name="1ère division Chypre",
        league_url="https://www.coteur.com/cotes/foot/chypre/1ere-division",
        display_name="1ère division Chypre"
    )
