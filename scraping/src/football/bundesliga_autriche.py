# scraping/src/football/bundesliga_autriche.py

from ._scraper_utils import scrape_league


def scrape_bundesliga_autriche():
    """Scrape Bundesliga Autriche"""
    return scrape_league(
        league_name="Bundesliga Autriche",
        league_url="https://www.coteur.com/cotes/foot/autriche/bundesliga",
        display_name="Bundesliga Autriche"
    )
