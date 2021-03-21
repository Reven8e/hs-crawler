from bs4 import BeautifulSoup
import pandas as pd
import requests


class scrape_keywords:
    def __init__(self):
        self.url = "https://www.ebay.com/"
        self.keywords = []
        self.df = pd.DataFrame()
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"}
        self.urls = []
        self.f = 0
    

    def homepage(self):
        req = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(req.text, 'lxml')
        li = soup.find_all("li", {"class": 'hl-cat-nav__js-tab'})
        for l in li:
            link = l.find("a", href=True)
            self.urls.append(link['href'])
            navs = l.find_all("nav", {"class": "hl-cat-nav__sub-cat-col"})
            
            try:
                popular = navs[0].find_all("li")
                for key in popular:
                    keyword = key.find("a", {"class": "hl-cat-nav__js-link"})
                    print(keyword.text)
                    self.f += 1
            except AttributeError and IndexError as e:
                print(e)

            try:
                categories = navs[1].find_all("li")
                for key in categories:
                    keyword = key.find("a", {"class": "hl-cat-nav__js-link"})
                    print(keyword.text)
                    self.f += 1
            except AttributeError and IndexError as e:
                print(e)  

        try:
            self.urls.remove("https://www.ebay.com/globaldeals")
            self.urls.remove("https://export.ebay.com/en/")
        except:
            pass

        self.by_urls()         


    def by_urls(self):
        for url in self.urls:
            print("-"*10 + url + "-"*10)
            try:
                req = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(req.text, 'lxml')
                table = soup.find("section", {'class': "b-module b-list b-categorynavigations b-display--landscape"})
                keys = table.find_all("li")
                for key in keys:
                    keyword = key.find("a")
                    print(keyword.text)
                    self.f += 1
            except AttributeError:
                table = soup.find("section", {"class": 'b-module b-list b-speciallinks b-display--landscape'})
                keys = table.find_all("li")
                for key in keys:
                    li = key.find_all('li')
                    for i in li:
                        keyword = i.find('a')
                        print(keyword.text)
                        self.f += 1
            
            except requests.exceptions.TooManyRedirects:
                pass

        print(self.f)


    def one_url(self):
        req = requests.get("https://ebay.com/b/Electronics/bn_7000259124")
        soup = BeautifulSoup(req.text, 'lxml')
        table = soup.find("section", {'class': "b-module b-list b-categorynavigations b-display--landscape"})
        


scrape_keywords().homepage()