from bs4 import BeautifulSoup
import pandas as pd
import requests


class Ebay_Scraper:
    def __init__(self):
        self.url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw={0}&_sacat=0&_ipg=200&_pgn={1}"
        self.df = pd.DataFrame()
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"}
        self.stop = False
        self.products = []
        self.num = 0

    
    def scrape(self, keyword, num):
        url = self.url
        try:
            req = requests.get(url.format(keyword, num), headers=self.headers)
            soup = BeautifulSoup(req.text, 'lxml')
            ul = soup.find("ul", {'class': "srp-results srp-list clearfix"})
            if ul is None: 
                self.stop = True
                return
            for i in range(1, 200):
                box = ul.find('li', {'data-view': f"mi:1686|iid:{i}"})
                name = box.find('a', {'class': "s-item__link"})
                self.products.append(name.text)

        except AttributeError:
            pass
        except Exception as e:
            print(e)
    

    def main(self):
        keywords = pd.read_csv("keywords.csv")
        for key in keywords["Keywords"]:
            print(key)
            self.stop = False
            i = 0
            while self.stop is False and i < 6:
                i += 1
                print(i)
                self.scrape(key, i)

        self.df["Products"] = self.products
        self.df.drop_duplicates(subset ="Products",
                     keep= False, inplace= True)
        self.df.to_csv("products.csv", index=False)

