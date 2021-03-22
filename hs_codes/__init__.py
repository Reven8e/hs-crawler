from .keywords import Scrape_Keywords
from .products import Ebay_Scraper
from .google_crawler import Google

__version__ = 0.1


def start():
    print("[1] Start Ebay Keywords Scraper")
    print("[2] Start Ebay Products Scraper by Keywords (keywords.csv)")
    print("[3] Start Google HS Codes Crawler by Products (prodocuts.csv)")
    option = int(input("\n: "))

    if option == 1:
        Scrape_Keywords().homepage()
    elif option == 2:
        Ebay_Scraper().main()
    elif option == 3:
        Google().main()