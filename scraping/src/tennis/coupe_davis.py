# scraping/src/tennis/coupe_davis.py

from ._scraper_utils import scrape_league


def scrape_coupe_davis():
    """Scrape Coupe Davis"""
    return scrape_league(
        league_name="Coupe Davis",
        league_url="https://www.coteur.com/cotes/tennis/monde/coupe-davis",
        display_name="Coupe Davis"
    )
