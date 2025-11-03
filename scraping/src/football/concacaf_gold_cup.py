# scraping/src/football/concacaf_gold_cup.py

from ._scraper_utils import scrape_league


def scrape_concacaf_gold_cup():
    """Scrape CONCACAF Gold Cup"""
    return scrape_league(
        league_name="CONCACAF Gold Cup",
        league_url="https://www.coteur.com/cotes/foot/amerique/concacaf-gold-cup",
        display_name="CONCACAF Gold Cup"
    )
