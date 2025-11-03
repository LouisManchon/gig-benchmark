# scraping/src/football/super_league_maroc.py

from ._scraper_utils import scrape_league


def scrape_super_league_maroc():
    """Scrape Super League Maroc"""
    return scrape_league(
        league_name="Super League Maroc",
        league_url="https://www.coteur.com/cotes/foot/maroc/super-league-1",
        display_name="Super League Maroc"
    )
