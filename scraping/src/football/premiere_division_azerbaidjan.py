# scraping/src/football/premiere_division_azerbaidjan.py

from ._scraper_utils import scrape_league


def scrape_premiere_division_azerbaidjan():
    """Scrape Première Division Azerbaïdjan"""
    return scrape_league(
        league_name="Première Division Azerbaïdjan",
        league_url="https://www.coteur.com/cotes/foot/azerbaidjan/premiere-division-1",
        display_name="Première Division Azerbaïdjan"
    )
