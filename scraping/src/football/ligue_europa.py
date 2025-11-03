# scraping/src/football/ligue_europa.py

from ._scraper_utils import scrape_league


def scrape_ligue_europa():
    """Scrape Ligue Europa"""
    return scrape_league(
        league_name="Ligue Europa",
        league_url="https://www.coteur.com/cotes/foot/europe/ligue-europa-1",
        display_name="Ligue Europa"
    )
