# scraping/src/football/bundesliga.py

from ._scraper_utils import scrape_league


def scrape_bundesliga():
    """Scrape Bundesliga"""
    return scrape_league(
        league_name="Bundesliga",
        league_url="https://www.coteur.com/cotes/foot/allemagne/bundesliga-d1",
        display_name="Bundesliga"
    )
