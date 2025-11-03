# scraping/src/tennis/atp_los_cabos.py

from ._scraper_utils import scrape_league


def scrape_atp_los_cabos():
    """Scrape ATP Los Cabos"""
    return scrape_league(
        league_name="ATP Los Cabos",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-los-cabos",
        display_name="ATP Los Cabos"
    )
