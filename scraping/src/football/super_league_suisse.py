# scraping/src/football/super_league_suisse.py

from ._scraper_utils import scrape_league


def scrape_super_league_suisse():
    """Scrape Super League Suisse"""
    return scrape_league(
        league_name="Super League Suisse",
        league_url="https://www.coteur.com/cotes/foot/suisse/super-league",
        display_name="Super League Suisse"
    )
