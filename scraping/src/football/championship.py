# scraping/src/football/championship.py

from ._scraper_utils import scrape_league


def scrape_championship():
    """Scrape Championship"""
    return scrape_league(
        league_name="Championship",
        league_url="https://www.coteur.com/cotes/foot/angleterre/the-championship",
        display_name="Championship"
    )
