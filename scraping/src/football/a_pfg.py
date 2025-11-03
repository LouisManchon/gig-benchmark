# scraping/src/football/a_pfg.py

from ._scraper_utils import scrape_league


def scrape_a_pfg():
    """Scrape A PFG"""
    return scrape_league(
        league_name="A PFG",
        league_url="https://www.coteur.com/cotes/foot/bulgarie/a-pfg",
        display_name="A PFG"
    )
