# scraping/src/rugby/top_14.py

from ._scraper_utils import scrape_league


def scrape_top_14():
    """Scrape Top 14"""
    return scrape_league(
        league_name="Top 14",
        league_url="https://www.coteur.com/cotes/rugby/france/top-14",
        display_name="Top 14"
    )
