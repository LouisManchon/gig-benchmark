# scraping/src/basketball/bundesliga.py

from ._scraper_utils import scrape_league


def scrape_bundesliga_basketball():
    """Scrape Bundesliga"""
    return scrape_league(
        league_name="Bundesliga",
        league_url="https://www.coteur.com/cotes/basket/allemagne/bundesliga-1",
        display_name="Bundesliga"
    )
