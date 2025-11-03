# scraping/src/football/division_1_algerie.py

from ._scraper_utils import scrape_league


def scrape_division_1_algerie():
    """Scrape Division 1 Algérie"""
    return scrape_league(
        league_name="Division 1 Algérie",
        league_url="https://www.coteur.com/cotes/foot/algerie/division-1-1",
        display_name="Division 1 Algérie"
    )
