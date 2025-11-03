# scraping/src/football/winner_league.py

from ._scraper_utils import scrape_league


def scrape_winner_league():
    """Scrape Winner League"""
    return scrape_league(
        league_name="Winner League",
        league_url="https://www.coteur.com/cotes/foot/israel/winner-league",
        display_name="Winner League"
    )
