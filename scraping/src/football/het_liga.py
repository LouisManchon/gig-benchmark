# scraping/src/football/het_liga.py

from ._scraper_utils import scrape_league


def scrape_het_liga():
    """Scrape HET Liga"""
    return scrape_league(
        league_name="HET Liga",
        league_url="https://www.coteur.com/cotes/foot/republique-tcheque/het-liga",
        display_name="HET Liga"
    )
