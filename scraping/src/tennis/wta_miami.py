# scraping/src/tennis/wta_miami.py

from ._scraper_utils import scrape_league


def scrape_wta_miami():
    """Scrape WTA Miami"""
    return scrape_league(
        league_name="WTA Miami",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-miami",
        display_name="WTA Miami"
    )
