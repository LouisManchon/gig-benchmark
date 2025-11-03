# scraping/src/tennis/atp_london.py

from ._scraper_utils import scrape_league


def scrape_atp_london():
    """Scrape ATP London"""
    return scrape_league(
        league_name="ATP London",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-londres-queens",
        display_name="ATP London"
    )
