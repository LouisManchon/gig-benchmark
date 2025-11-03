# scraping/src/football/primera_division_argentine.py

from ._scraper_utils import scrape_league


def scrape_primera_division_argentine():
    """Scrape Primera Division Argentine"""
    return scrape_league(
        league_name="Primera Division Argentine",
        league_url="https://www.coteur.com/cotes/foot/argentine/primera-division-2",
        display_name="Primera Division Argentine"
    )
