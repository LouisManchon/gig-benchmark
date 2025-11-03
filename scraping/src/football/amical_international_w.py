# scraping/src/football/amical_international_w.py

from ._scraper_utils import scrape_league


def scrape_amical_international_w():
    """Scrape Amical International W"""
    return scrape_league(
        league_name="Amical International W",
        league_url="https://www.coteur.com/cotes/foot/monde/matches-amicaux-internationaux-f",
        display_name="Amical International W"
    )
