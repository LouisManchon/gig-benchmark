# scraping/src/tennis/atp_kitzbuhel.py

from ._scraper_utils import scrape_league


def scrape_atp_kitzbuhel():
    """Scrape ATP Kitzbuhel"""
    return scrape_league(
        league_name="ATP Kitzbuhel",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-kitzbuhel-1",
        display_name="ATP Kitzbuhel"
    )
