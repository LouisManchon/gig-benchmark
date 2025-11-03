# scraping/src/tennis/atp_cincinnati.py

from ._scraper_utils import scrape_league


def scrape_atp_cincinnati():
    """Scrape ATP Cincinnati"""
    return scrape_league(
        league_name="ATP Cincinnati",
        league_url="https://www.coteur.com/cotes/tennis/monde/masters-cincinnati",
        display_name="ATP Cincinnati"
    )
