# scraping/src/football/copa_libertadores.py

from ._scraper_utils import scrape_league


def scrape_copa_libertadores():
    """Scrape Copa Libertadores"""
    return scrape_league(
        league_name="Copa Libertadores",
        league_url="https://www.coteur.com/cotes/foot/amerique-du-sud/copa-libertadores",
        display_name="Copa Libertadores"
    )
