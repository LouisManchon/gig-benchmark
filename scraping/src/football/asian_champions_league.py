# scraping/src/football/asian_champions_league.py

from ._scraper_utils import scrape_league


def scrape_asian_champions_league():
    """Scrape Asian Champions League"""
    return scrape_league(
        league_name="Asian Champions League",
        league_url="https://www.coteur.com/cotes/foot/monde-1/ldc-dasie-phase-finale",
        display_name="Asian Champions League"
    )
