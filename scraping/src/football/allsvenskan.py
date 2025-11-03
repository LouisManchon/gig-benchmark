# scraping/src/football/allsvenskan.py

from ._scraper_utils import scrape_league


def scrape_allsvenskan():
    """Scrape Allsvenskan"""
    return scrape_league(
        league_name="Allsvenskan",
        league_url="https://www.coteur.com/cotes/foot/suede/allsvenskan",
        display_name="Allsvenskan"
    )
