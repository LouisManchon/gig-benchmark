# scraping/src/football/prvaliga.py

from ._scraper_utils import scrape_league


def scrape_prvaliga():
    """Scrape PrvaLiga"""
    return scrape_league(
        league_name="PrvaLiga",
        league_url="https://www.coteur.com/cotes/foot/slovenie/prvaliga",
        display_name="PrvaLiga"
    )
