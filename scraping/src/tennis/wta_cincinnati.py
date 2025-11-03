# scraping/src/tennis/wta_cincinnati.py

from ._scraper_utils import scrape_league


def scrape_wta_cincinnati():
    """Scrape WTA Cincinnati"""
    return scrape_league(
        league_name="WTA Cincinnati",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-cincinnati",
        display_name="WTA Cincinnati"
    )
