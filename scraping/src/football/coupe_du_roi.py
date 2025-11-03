# scraping/src/football/coupe_du_roi.py

from ._scraper_utils import scrape_league


def scrape_coupe_du_roi():
    """Scrape Coupe du roi"""
    return scrape_league(
        league_name="Coupe du roi",
        league_url="https://www.coteur.com/cotes/foot/espagne/coupe-du-roi",
        display_name="Coupe du roi"
    )
