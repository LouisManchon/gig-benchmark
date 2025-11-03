# scraping/src/tennis/atp_hertogenbosch.py

from ._scraper_utils import scrape_league


def scrape_atp_hertogenbosch():
    """Scrape ATP Hertogenbosch"""
    return scrape_league(
        league_name="ATP Hertogenbosch",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-s-hertogenbosch",
        display_name="ATP Hertogenbosch"
    )
