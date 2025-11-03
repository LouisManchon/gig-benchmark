# scraping/src/tennis/wta_jiujiang.py

from ._scraper_utils import scrape_league


def scrape_wta_jiujiang():
    """Scrape WTA Jiujiang"""
    return scrape_league(
        league_name="WTA Jiujiang",
        league_url="https://www.coteur.com/cotes/tennis/monde-1/wta-jiujiang",
        display_name="WTA Jiujiang"
    )
