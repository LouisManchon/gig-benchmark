# scraping/src/football/premier_league.py

from ._scraper_utils import scrape_league


def scrape_premier_league():
    """Scrape Premier League"""
    return scrape_league(
        league_name="Premier League",
        league_url="https://www.coteur.com/cotes/foot/angleterre/premier-league",
        display_name="Premier League"
    )
