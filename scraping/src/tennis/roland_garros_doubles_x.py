# scraping/src/tennis/roland_garros_doubles_x.py

from ._scraper_utils import scrape_league


def scrape_roland_garros_doubles_x():
    """Scrape Roland-Garros Doubles X"""
    return scrape_league(
        league_name="Roland-Garros Doubles X",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-roland-garros-doubles-mixte",
        display_name="Roland-Garros Doubles X"
    )
