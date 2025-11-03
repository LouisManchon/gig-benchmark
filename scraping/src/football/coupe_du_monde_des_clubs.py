# scraping/src/football/coupe_du_monde_des_clubs.py

from ._scraper_utils import scrape_league


def scrape_coupe_du_monde_des_clubs():
    """Scrape Coupe du monde des Clubs"""
    return scrape_league(
        league_name="Coupe du monde des Clubs",
        league_url="https://www.coteur.com/cotes/foot/monde/coupe-du-monde-des-clubs",
        display_name="Coupe du monde des Clubs"
    )
