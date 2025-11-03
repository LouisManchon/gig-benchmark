# scraping/src/tennis/atp_winston_salem.py

from ._scraper_utils import scrape_league


def scrape_atp_winston_salem():
    """Scrape ATP Winston-Salem"""
    return scrape_league(
        league_name="ATP Winston-Salem",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-winston-salem",
        display_name="ATP Winston-Salem"
    )
