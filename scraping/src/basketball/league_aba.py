# scraping/src/basketball/league_aba.py

from ._scraper_utils import scrape_league


def scrape_league_aba():
    """Scrape League ABA"""
    return scrape_league(
        league_name="League ABA",
        league_url="https://www.coteur.com/cotes/basket/europe/nlb-league-aba",
        display_name="League ABA"
    )
