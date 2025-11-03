# scraping/src/tennis/roland_garros_doubles_m.py

from ._scraper_utils import scrape_league


def scrape_roland_garros_doubles_m():
    """Scrape Roland-Garros Doubles M"""
    return scrape_league(
        league_name="Roland-Garros Doubles M",
        league_url="https://www.coteur.com/cotes/tennis/monde/atp-roland-garros-doubles",
        display_name="Roland-Garros Doubles M"
    )
