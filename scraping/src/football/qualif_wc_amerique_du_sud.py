# scraping/src/football/qualif_wc_amerique_du_sud.py

from ._scraper_utils import scrape_league


def scrape_qualif_wc_amerique_du_sud():
    """Scrape Qualif WC Amérique du Sud"""
    return scrape_league(
        league_name="Qualif WC Amérique du Sud",
        league_url="https://www.coteur.com/cotes/foot/amerique-du-sud/qualification-coupe-du-monde-zone-amsud",
        display_name="Qualif WC Amérique du Sud"
    )
