# scraping/src/football/k_league_1.py

from ._scraper_utils import scrape_league


def scrape_k_league_1():
    """Scrape K-League 1"""
    return scrape_league(
        league_name="K-League 1",
        league_url="https://www.coteur.com/cotes/foot/coree-du-sud/k-league-1",
        display_name="K-League 1"
    )
