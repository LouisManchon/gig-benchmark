# scraping/src/tennis/atp_bucharest.py

from ._scraper_utils import scrape_league


def scrape_atp_bucharest():
    """Scrape ATP Bucharest"""
    return scrape_league(
        league_name="ATP Bucharest",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-bucarest",
        display_name="ATP Bucharest"
    )
