# scraping/src/football/casino_eredivisie.py

from ._scraper_utils import scrape_league


def scrape_casino_eredivisie():
    """Scrape Casino Eredivisie"""
    return scrape_league(
        league_name="Casino Eredivisie",
        league_url="https://www.coteur.com/cotes/foot/pays-bas/casino-eredivisie",
        display_name="Casino Eredivisie"
    )
