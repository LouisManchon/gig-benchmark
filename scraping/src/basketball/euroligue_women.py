# scraping/src/basketball/euroligue_women.py

from ._scraper_utils import scrape_league


def scrape_euroligue_women():
    """Scrape Euroligue Women"""
    return scrape_league(
        league_name="Euroligue Women",
        league_url="https://www.coteur.com/cotes/basket/europe/euroligue-femmes",
        display_name="Euroligue Women"
    )
