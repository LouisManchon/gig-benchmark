# scraping/src/football/super_league_grece.py

from ._scraper_utils import scrape_league


def scrape_super_league_grece():
    """Scrape Super League Grèce"""
    return scrape_league(
        league_name="Super League Grèce",
        league_url="https://www.coteur.com/cotes/foot/grece/super-league-2",
        display_name="Super League Grèce"
    )
