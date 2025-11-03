# scraping/src/rugby/pro_d2.py

from ._scraper_utils import scrape_league


def scrape_pro_d2():
    """Scrape Pro D2"""
    return scrape_league(
        league_name="Pro D2",
        league_url="https://www.coteur.com/cotes/rugby/france/pro-d2",
        display_name="Pro D2"
    )
