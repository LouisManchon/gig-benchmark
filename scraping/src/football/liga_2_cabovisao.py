# scraping/src/football/liga_2_cabovisao.py

from ._scraper_utils import scrape_league


def scrape_liga_2_cabovisao():
    """Scrape Liga 2 Cabovisao"""
    return scrape_league(
        league_name="Liga 2 Cabovisao",
        league_url="https://www.coteur.com/cotes/foot/portugal/liga-2-cabovisao",
        display_name="Liga 2 Cabovisao"
    )
