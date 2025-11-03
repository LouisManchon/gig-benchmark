# scraping/src/football/premier_division_irlande.py

from ._scraper_utils import scrape_league


def scrape_premier_division_irlande():
    """Scrape Premier Division Irlande"""
    return scrape_league(
        league_name="Premier Division Irlande",
        league_url="https://www.coteur.com/cotes/foot/rep-dirlande/premier-division",
        display_name="Premier Division Irlande"
    )
