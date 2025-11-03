# scraping/src/football/bov_premier_division.py

from ._scraper_utils import scrape_league


def scrape_bov_premier_division():
    """Scrape BOV Premier Division"""
    return scrape_league(
        league_name="BOV Premier Division",
        league_url="https://www.coteur.com/cotes/foot/malte/bov-premier-division",
        display_name="BOV Premier Division"
    )
