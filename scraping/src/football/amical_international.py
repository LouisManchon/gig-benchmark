# scraping/src/football/amical_international.py

from ._scraper_utils import scrape_league


def scrape_amical_international():
    """Scrape Amical International"""
    return scrape_league(
        league_name="Amical International",
        league_url="https://www.coteur.com/cotes/foot/monde/international-matchs-amicaux",
        display_name="Amical International"
    )
