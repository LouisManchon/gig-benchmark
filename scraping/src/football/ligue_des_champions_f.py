# scraping/src/football/ligue_des_champions_f.py

from ._scraper_utils import scrape_league


def scrape_ligue_des_champions_f():
    """Scrape Ligue des Champions F"""
    return scrape_league(
        league_name="Ligue des Champions F",
        league_url="https://www.coteur.com/cotes/foot/europe/ligue-des-champions-f",
        display_name="Ligue des Champions F"
    )
