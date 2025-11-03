# scraping/src/tennis/atp_bruxelles.py

from ._scraper_utils import scrape_league


def scrape_atp_bruxelles():
    """Scrape ATP Bruxelles"""
    return scrape_league(
        league_name="ATP Bruxelles",
        league_url="https://www.coteur.com/cotes/tennis/monde-1/atp-bruxelles",
        display_name="ATP Bruxelles"
    )
