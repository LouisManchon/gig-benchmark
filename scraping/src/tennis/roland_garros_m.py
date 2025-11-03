# scraping/src/tennis/roland_garros_m.py

from ._scraper_utils import scrape_league


def scrape_roland_garros_m():
    """Scrape Roland-Garros M"""
    return scrape_league(
        league_name="Roland-Garros M",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-roland-garros",
        display_name="Roland-Garros M"
    )
