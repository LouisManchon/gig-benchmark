# scraping/src/football/j_league.py

from ._scraper_utils import scrape_league


def scrape_j_league():
    """Scrape J. League"""
    return scrape_league(
        league_name="J. League",
        league_url="https://www.coteur.com/cotes/foot/japon/j-league",
        display_name="J. League"
    )
