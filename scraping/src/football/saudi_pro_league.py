# scraping/src/football/saudi_pro_league.py

from ._scraper_utils import scrape_league


def scrape_saudi_pro_league():
    """Scrape Saudi Pro League"""
    return scrape_league(
        league_name="Saudi Pro League",
        league_url="https://www.coteur.com/cotes/foot/arabie-saoudite/saudi-pro-league",
        display_name="Saudi Pro League"
    )
