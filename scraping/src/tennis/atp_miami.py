# scraping/src/tennis/atp_miami.py

from ._scraper_utils import scrape_league


def scrape_atp_miami():
    """Scrape ATP Miami"""
    return scrape_league(
        league_name="ATP Miami",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-masters-miami",
        display_name="ATP Miami"
    )
