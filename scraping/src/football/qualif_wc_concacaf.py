# scraping/src/football/qualif_wc_concacaf.py

from ._scraper_utils import scrape_league


def scrape_qualif_wc_concacaf():
    """Scrape Qualif WC CONCACAF"""
    return scrape_league(
        league_name="Qualif WC CONCACAF",
        league_url="https://www.coteur.com/cotes/foot/amerique/qualification-coupe-du-monde-concacaf",
        display_name="Qualif WC CONCACAF"
    )
