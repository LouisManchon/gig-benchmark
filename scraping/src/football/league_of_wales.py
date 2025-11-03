# scraping/src/football/league_of_wales.py

from ._scraper_utils import scrape_league


def scrape_league_of_wales():
    """Scrape League Of Wales"""
    return scrape_league(
        league_name="League Of Wales",
        league_url="https://www.coteur.com/cotes/foot/pays-de-galles/league-of-wales",
        display_name="League Of Wales"
    )
