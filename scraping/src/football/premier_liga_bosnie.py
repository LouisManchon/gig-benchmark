# scraping/src/football/premier_liga_bosnie.py

from ._scraper_utils import scrape_league


def scrape_premier_liga_bosnie():
    """Scrape Premier Liga Bosnie"""
    return scrape_league(
        league_name="Premier Liga Bosnie",
        league_url="https://www.coteur.com/cotes/foot/bosnie-herzegovine/premier-liga-1",
        display_name="Premier Liga Bosnie"
    )
