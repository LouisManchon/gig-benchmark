# scraping/src/football/superligaen.py

from ._scraper_utils import scrape_league


def scrape_superligaen():
    """Scrape Superligaen"""
    return scrape_league(
        league_name="Superligaen",
        league_url="https://www.coteur.com/cotes/foot/danemark/superligaen",
        display_name="Superligaen"
    )
