# scraping/src/football/community_shield.py

from ._scraper_utils import scrape_league


def scrape_community_shield():
    """Scrape Community Shield"""
    return scrape_league(
        league_name="Community Shield",
        league_url="https://www.coteur.com/cotes/foot/angleterre/community-shield",
        display_name="Community Shield"
    )
