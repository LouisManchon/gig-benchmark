# scraping/src/football/ligue_des_nations.py

from ._scraper_utils import scrape_league


def scrape_ligue_des_nations():
    """Scrape Ligue des Nations"""
    return scrape_league(
        league_name="Ligue des Nations",
        league_url="https://www.coteur.com/cotes/foot/europe/ligue-des-nations",
        display_name="Ligue des Nations"
    )
