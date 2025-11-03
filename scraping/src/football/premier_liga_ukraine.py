# scraping/src/football/premier_liga_ukraine.py

from ._scraper_utils import scrape_league


def scrape_premier_liga_ukraine():
    """Scrape Premier Liga Ukraine"""
    return scrape_league(
        league_name="Premier Liga Ukraine",
        league_url="https://www.coteur.com/cotes/foot/ukraine/premier-liga",
        display_name="Premier Liga Ukraine"
    )
