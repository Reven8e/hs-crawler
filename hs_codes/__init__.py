from .main_scraper import scraper

__version__ = 0.01


def start():
    scraper("851712").getter()