# scraping/src/basketball/a1.py

from ._scraper_utils import scrape_league


def scrape_a1():
    """Scrape A1"""
    return scrape_league(
        league_name="A1",
        league_url="https://www.coteur.com/cotes/basket/grece/a1-hommes",
        display_name="A1"
    )
