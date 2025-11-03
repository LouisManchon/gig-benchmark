# scraping/src/football/premiership_ecosse.py

from ._scraper_utils import scrape_league


def scrape_premiership_ecosse():
    """Scrape Premiership Ecosse"""
    return scrape_league(
        league_name="Premiership Ecosse",
        league_url="https://www.coteur.com/cotes/foot/ecosse/premiership",
        display_name="Premiership Ecosse"
    )
