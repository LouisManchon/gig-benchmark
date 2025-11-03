# scraping/src/football/super_league_chine.py

from ._scraper_utils import scrape_league


def scrape_super_league_chine():
    """Scrape Super League Chine"""
    return scrape_league(
        league_name="Super League Chine",
        league_url="https://www.coteur.com/cotes/foot/chine/super-league-5",
        display_name="Super League Chine"
    )
