# scraping/src/football/concacaf_ligue_des_nations.py

from ._scraper_utils import scrape_league


def scrape_concacaf_ligue_des_nations():
    """Scrape CONCACAF Ligue des Nations"""
    return scrape_league(
        league_name="CONCACAF Ligue des Nations",
        league_url="https://www.coteur.com/cotes/foot/monde/concacaf-ligue-des-nations",
        display_name="CONCACAF Ligue des Nations"
    )
