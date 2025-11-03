# scraping/src/football/super_ligi.py

from ._scraper_utils import scrape_league


def scrape_super_ligi():
    """Scrape Super Ligi"""
    return scrape_league(
        league_name="Super Ligi",
        league_url="https://www.coteur.com/cotes/foot/turquie/super-ligi",
        display_name="Super Ligi"
    )
