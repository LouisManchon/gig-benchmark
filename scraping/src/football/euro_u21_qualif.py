# scraping/src/football/euro_u21_qualif.py

from ._scraper_utils import scrape_league


def scrape_euro_u21_qualif():
    """Scrape Euro U21 Qualif"""
    return scrape_league(
        league_name="Euro U21 Qualif",
        league_url="https://www.coteur.com/cotes/foot/europe/championnat-deurope-u21-qualification",
        display_name="Euro U21 Qualif"
    )
