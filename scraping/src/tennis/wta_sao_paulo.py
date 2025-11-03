# scraping/src/tennis/wta_sao_paulo.py

from ._scraper_utils import scrape_league


def scrape_wta_sao_paulo():
    """Scrape WTA Sao Paulo"""
    return scrape_league(
        league_name="WTA Sao Paulo",
        league_url="https://www.coteur.com/cotes/tennis/monde-1/wta-sao-paulo",
        display_name="WTA Sao Paulo"
    )
