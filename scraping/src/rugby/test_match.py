# scraping/src/rugby/test_match.py

from ._scraper_utils import scrape_league


def scrape_test_match():
    """Scrape Test-Match"""
    return scrape_league(
        league_name="Test-Match",
        league_url="https://www.coteur.com/cotes/rugby/monde/international-test-match",
        display_name="Test-Match"
    )
