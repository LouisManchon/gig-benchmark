# scraping/src/basketball/eurocup_women.py

from ._scraper_utils import scrape_league


def scrape_eurocup_women():
    """Scrape Eurocup Women"""
    return scrape_league(
        league_name="Eurocup Women",
        league_url="https://www.coteur.com/cotes/basket/europe/eurocoupe-f",
        display_name="Eurocup Women"
    )
