from bs4 import BeautifulSoup
import requests


class scraper:
    def __init__(self, code):
        self.url = f"https://www.hs-codes.com/?c={code}"

    
    def getter(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, "lxml")
        div = soup.find("div", {"class": "pure-u-1 pure-u-md-16-24"})
        a = div.find("a", {"class": "results_list"})
        return a.text


# scraper("851712").getter()