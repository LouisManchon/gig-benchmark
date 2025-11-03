# scraping/src/football/serie_a_equateur.py

from ._scraper_utils import scrape_league


def scrape_serie_a_equateur():
    """Scrape Série A Equateur"""
    return scrape_league(
        league_name="Série A Equateur",
        league_url="https://www.coteur.com/cotes/foot/equateur/serie-a-3",
        display_name="Série A Equateur"
    )
