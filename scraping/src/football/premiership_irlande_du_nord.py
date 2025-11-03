# scraping/src/football/premiership_irlande_du_nord.py

from ._scraper_utils import scrape_league


def scrape_premiership_irlande_du_nord():
    """Scrape Premiership Irlande du Nord"""
    return scrape_league(
        league_name="Premiership Irlande du Nord",
        league_url="https://www.coteur.com/cotes/foot/irlande-du-nord/premiership-2",
        display_name="Premiership Irlande du Nord"
    )
