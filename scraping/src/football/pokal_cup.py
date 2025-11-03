# scraping/src/football/pokal_cup.py

from ._scraper_utils import scrape_league


def scrape_pokal_cup():
    """Scrape Pokal Cup"""
    return scrape_league(
        league_name="Pokal Cup",
        league_url="https://www.coteur.com/cotes/foot/allemagne/pokal-cup",
        display_name="Pokal Cup"
    )
