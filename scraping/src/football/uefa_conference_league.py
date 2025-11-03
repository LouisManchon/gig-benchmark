# scraping/src/football/uefa_conference_league.py

from ._scraper_utils import scrape_league


def scrape_uefa_conference_league():
    """Scrape UEFA Conference League"""
    return scrape_league(
        league_name="UEFA Conference League",
        league_url="https://www.coteur.com/cotes/foot/europe/uefa-conference-league",
        display_name="UEFA Conference League"
    )
