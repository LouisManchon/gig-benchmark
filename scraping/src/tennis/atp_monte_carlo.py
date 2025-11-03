# scraping/src/tennis/atp_monte_carlo.py

from ._scraper_utils import scrape_league


def scrape_atp_monte_carlo():
    """Scrape ATP Monte-Carlo"""
    return scrape_league(
        league_name="ATP Monte-Carlo",
        league_url="https://www.coteur.com/cotes/tennis/monde/masters-atp-monte-carlo",
        display_name="ATP Monte-Carlo"
    )
