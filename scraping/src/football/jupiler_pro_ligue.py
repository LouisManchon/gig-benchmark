# scraping/src/football/jupiler_pro_ligue.py

from ._scraper_utils import scrape_league


def scrape_jupiler_pro_ligue():
    """Scrape Jupiler Pro Ligue"""
    return scrape_league(
        league_name="Jupiler Pro Ligue",
        league_url="https://www.coteur.com/cotes/foot/belgique/jupiler-pro-ligue",
        display_name="Jupiler Pro Ligue"
    )
