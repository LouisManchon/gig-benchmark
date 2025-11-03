# scraping/src/football/a_league.py

from ._scraper_utils import scrape_league


def scrape_a_league():
    """Scrape A-League"""
    return scrape_league(
        league_name="A-League",
        league_url="https://www.coteur.com/cotes/foot/australie/a-league",
        display_name="A-League"
    )
