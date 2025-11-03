# scraping/src/football/copa_sudamericana.py

from ._scraper_utils import scrape_league


def scrape_copa_sudamericana():
    """Scrape Copa Sudamericana"""
    return scrape_league(
        league_name="Copa Sudamericana",
        league_url="https://www.coteur.com/cotes/foot/amerique-du-sud/copa-sudamericana",
        display_name="Copa Sudamericana"
    )
