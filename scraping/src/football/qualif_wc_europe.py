# scraping/src/football/qualif_wc_europe.py

from ._scraper_utils import scrape_league


def scrape_qualif_wc_europe():
    """Scrape Qualif WC Europe"""
    return scrape_league(
        league_name="Qualif WC Europe",
        league_url="https://www.coteur.com/cotes/foot/monde/qualifications-coupe-du-monde-europe",
        display_name="Qualif WC Europe"
    )
