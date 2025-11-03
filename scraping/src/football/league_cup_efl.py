# scraping/src/football/league_cup_efl.py

from ._scraper_utils import scrape_league


def scrape_league_cup_efl():
    """Scrape League Cup EFL"""
    return scrape_league(
        league_name="League Cup EFL",
        league_url="https://www.coteur.com/cotes/foot/angleterre/league-cup-efl",
        display_name="League Cup EFL"
    )
