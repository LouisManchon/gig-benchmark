# scraping/src/football/super_league_serbie.py

from ._scraper_utils import scrape_league


def scrape_super_league_serbie():
    """Scrape Super League Serbie"""
    return scrape_league(
        league_name="Super League Serbie",
        league_url="https://www.coteur.com/cotes/foot/serbie/super-league-3",
        display_name="Super League Serbie"
    )
