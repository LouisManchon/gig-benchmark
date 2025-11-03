# scraping/src/football/bundesliga_2.py

from ._scraper_utils import scrape_league


def scrape_bundesliga_2():
    """Scrape Bundesliga 2"""
    return scrape_league(
        league_name="Bundesliga 2",
        league_url="https://www.coteur.com/cotes/foot/allemagne/bundesliga-2",
        display_name="Bundesliga 2"
    )
