# scraping/src/football/liga_1_roumanie.py

from ._scraper_utils import scrape_league


def scrape_liga_1_roumanie():
    """Scrape Liga 1 Roumanie"""
    return scrape_league(
        league_name="Liga 1 Roumanie",
        league_url="https://www.coteur.com/cotes/foot/roumanie/liga-1",
        display_name="Liga 1 Roumanie"
    )
