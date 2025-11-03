# scraping/src/tennis/atp_geneve.py

from ._scraper_utils import scrape_league


def scrape_atp_geneve():
    """Scrape ATP Geneve"""
    return scrape_league(
        league_name="ATP Geneve",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-geneve",
        display_name="ATP Geneve"
    )
