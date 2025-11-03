# scraping/src/tennis/atp_chengdu.py

from ._scraper_utils import scrape_league


def scrape_atp_chengdu():
    """Scrape ATP Chengdu"""
    return scrape_league(
        league_name="ATP Chengdu",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-chengdu",
        display_name="ATP Chengdu"
    )
