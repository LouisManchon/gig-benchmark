# scraping/src/football/orange_ekstraklasa.py

from ._scraper_utils import scrape_league


def scrape_orange_ekstraklasa():
    """Scrape Orange Ekstraklasa"""
    return scrape_league(
        league_name="Orange Ekstraklasa",
        league_url="https://www.coteur.com/cotes/foot/pologne/orange-ekstraklasa",
        display_name="Orange Ekstraklasa"
    )
