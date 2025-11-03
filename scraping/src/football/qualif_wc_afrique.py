# scraping/src/football/qualif_wc_afrique.py

from ._scraper_utils import scrape_league


def scrape_qualif_wc_afrique():
    """Scrape Qualif WC Afrique"""
    return scrape_league(
        league_name="Qualif WC Afrique",
        league_url="https://www.coteur.com/cotes/foot/afrique/coupe-du-monde-qualifications-afrique",
        display_name="Qualif WC Afrique"
    )
