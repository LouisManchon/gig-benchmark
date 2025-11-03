# scraping/src/football/nb_i_hongrie.py

from ._scraper_utils import scrape_league


def scrape_nb_i_hongrie():
    """Scrape NB I Hongrie"""
    return scrape_league(
        league_name="NB I Hongrie",
        league_url="https://www.coteur.com/cotes/foot/hongrie/nb-i",
        display_name="NB I Hongrie"
    )
