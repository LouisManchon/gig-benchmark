# scraping/src/football/liga_mx.py

from ._scraper_utils import scrape_league


def scrape_liga_mx():
    """Scrape Liga MX"""
    return scrape_league(
        league_name="Liga MX",
        league_url="https://www.coteur.com/cotes/foot/mexique/primera-division-5",
        display_name="Liga MX"
    )
