# scraping/src/football/a_lyga.py

from ._scraper_utils import scrape_league


def scrape_a_lyga():
    """Scrape A Lyga"""
    return scrape_league(
        league_name="A Lyga",
        league_url="https://www.coteur.com/cotes/foot/lituanie/a-lyga",
        display_name="A Lyga"
    )
