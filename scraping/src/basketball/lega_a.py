# scraping/src/basketball/lega_a.py

from ._scraper_utils import scrape_league


def scrape_lega_a():
    """Scrape Lega A"""
    return scrape_league(
        league_name="Lega A",
        league_url="https://www.coteur.com/cotes/basket/italie/lega-a",
        display_name="Lega A"
    )
