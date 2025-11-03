# scraping/src/basketball/ligue_des_champions.py

from ._scraper_utils import scrape_league


def scrape_ligue_des_champions():
    """Scrape Ligue des Champions"""
    return scrape_league(
        league_name="Ligue des Champions",
        league_url="https://www.coteur.com/cotes/basket/europe/ligue-des-champions-2",
        display_name="Ligue des Champions"
    )
