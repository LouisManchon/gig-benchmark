# scraping/src/tennis/wta_finals_riyadh.py

from ._scraper_utils import scrape_league


def scrape_wta_finals_riyadh():
    """Scrape WTA Finals (Riyadh)"""
    return scrape_league(
        league_name="WTA Finals (Riyadh)",
        league_url="https://www.coteur.com/cotes/tennis/monde-1/wta-finals",
        display_name="WTA Finals (Riyadh)"
    )
