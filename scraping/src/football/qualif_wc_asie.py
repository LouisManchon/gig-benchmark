# scraping/src/football/qualif_wc_asie.py

from ._scraper_utils import scrape_league


def scrape_qualif_wc_asie():
    """Scrape Qualif WC Asie"""
    return scrape_league(
        league_name="Qualif WC Asie",
        league_url="https://www.coteur.com/cotes/foot/asie/qualification-coupe-du-monde-asie",
        display_name="Qualif WC Asie"
    )
