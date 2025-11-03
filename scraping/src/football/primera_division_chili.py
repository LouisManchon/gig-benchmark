# scraping/src/football/primera_division_chili.py

from ._scraper_utils import scrape_league


def scrape_primera_division_chili():
    """Scrape Primera Division Chili"""
    return scrape_league(
        league_name="Primera Division Chili",
        league_url="https://www.coteur.com/cotes/foot/chili/primera-division-4",
        display_name="Primera Division Chili"
    )
