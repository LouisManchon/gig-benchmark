# scraping/src/tennis/atp_shanghai.py

from ._scraper_utils import scrape_league


def scrape_atp_shanghai():
    """Scrape ATP Shanghai"""
    return scrape_league(
        league_name="ATP Shanghai",
        league_url="https://www.coteur.com/cotes/tennis/monde/masters-shanghai",
        display_name="ATP Shanghai"
    )
