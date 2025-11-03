# scraping/src/tennis/roland_garros_w.py

from ._scraper_utils import scrape_league


def scrape_roland_garros_w():
    """Scrape Roland-Garros W"""
    return scrape_league(
        league_name="Roland-Garros W",
        league_url="https://www.coteur.com/cotes/tennis/monde/wta-roland-garros",
        display_name="Roland-Garros W"
    )
