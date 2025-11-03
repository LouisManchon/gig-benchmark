# scraping/src/football/euro_femmes.py

from ._scraper_utils import scrape_league


def scrape_euro_femmes():
    """Scrape Euro Femmes"""
    return scrape_league(
        league_name="Euro Femmes",
        league_url="https://www.coteur.com/cotes/foot/europe/euro-femmes",
        display_name="Euro Femmes"
    )
