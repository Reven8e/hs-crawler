from bs4 import BeautifulSoup
import pandas as pd
from pandas.io.parsers import read_csv
import requests, re, json


class HS_Instructor:
    def __init__(self, where: int):
        url = "https://www.tariffnumber.com/2021/{0}"
        self.headers = headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"}

        r = requests.get(url.format(where), headers=headers)
        self.soup = BeautifulSoup(r.text, "lxml")
        self.codes = []
        self.desc = []
        self.df = pd.DataFrame()


    def sub(self):
        self.table = self.soup.find("div", {'class': 'col-md-9 col-12'})
        self.cols = self.table.find_all("div", {'class': 'mb-4 shadow'})


    def fixer(self, key: list):
        g = []
        while ' ' in key:
            key.remove(' ')
        while '' in key:
            key.remove('')
        while "\r\n" in key:
            key.remove('\r\n')
        while '"' in key:
            key.remove('')
        for k in key:
            g.append(k.replace("\n", "").replace("\r", "").replace(",", "").lower())
        final = " ".join(g)
        return final


    def title(self):
        for col in self.cols:
            code_cont = col.find("div", {"class": "rowheader"})
            code = code_cont.find("a")
            desc = col.find("div", {"class": "col-sm-9 col-lg-10"})

            desc_l = desc.text.split(" ")
            code_l = code.text.split(" ")
            d = self.fixer(desc_l)
            cod = self.fixer(code_l)
            self.desc.append(d)
            self.codes.append(cod)


    def body(self):
        for col in self.cols:
            groups = col.find_all("div", {'class': "rowgroup"})
            for group in groups:
                code = group.find("a", {"class": "text-nowrap"})
                desc = group.find("div", {"class": "col-sm-9 col-lg-10"})

                desc_l = desc.text.split(" ")
                code_l = code.text.split(" ")
                d = self.fixer(desc_l)
                cod = self.fixer(code_l)
                self.desc.append(d)
                self.codes.append(cod)
                
    
    def instructor(self):
        self.sub()
        self.title()
        self.body()
        print(self.codes[0])
        print(self.desc[0])

        self.df["Code"] = self.codes
        self.df["Description"] = self.desc
        self.df.to_csv("instructions.csv", index=False)



# HS_Instructor(85).instructor() # Enter hs code number here


df = read_csv('main.csv')


class Popular():
    def __init__(self, df):
        self.df = df
        self.dict = {}
        self.bad = ["for", "and", "a", "other", "or", "of", "excl", "the", "not", "as"]


    def find(self):
        for row in self.df.itertuples():
            self.splitter({row.Code: row.Description})
        return self.dict

    
    def splitter(self, obj: dict):
        w = ''.join([i for i in str(obj.values()) if not i.isdigit()])
        words = re.sub(r'[^\w]', ' ', w)
        words = words.split(" ")
        while '' in words:
            words.remove('')
        words.remove("dict_values")
        self.comp(words, list(obj.keys()))


    def comp(self, words: list, code):
        sort = {}
        for word in words:
            if word not in self.bad:
                if word in sort:
                    sort[word] += 1
                else:
                    sort[word] = 1
        
        top = sorted(sort, key=sort.get, reverse=True)[:6]
        self.dict[str(code[0])] = top


pop = Popular(df).find()


class Searcher():
    def __init__(self):
        self.url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw={0}&_sacat=0&_ipg=200&_pgn={1}"
        self.df = pd.DataFrame()
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"}
        self.products = []
        self.hs_codes = []
        self.categories = []
        self.stop = False

    
    def get_keywords(self):
        for code, keyword in pop.items():
            print(keyword)
            self.stop = False
            self.get_cats(code, keyword)
            return

    
    def get_cats(self, code, keyword):
        categories = []
        try:
            req = requests.get(self.url.format(f"{keyword[0]} {keyword[1]}", 1), headers=self.headers)
            print(self.url.format(f"{keyword[0]} {keyword[1]}", 1))
            soup = BeautifulSoup(req.text, 'lxml')

            cont = soup.find("ul", {'class': "srp-refine__category__list"})
            cats = cont.find_all("li")
            for cat in cats:
                names = cat.find_all("a")
                for n in names: categories.append(n.text.lower())

            if self.checker(keyword, categories) is True:
                self.scrape(soup, keyword)

        except AttributeError as e:
            print(e)
        except Exception as e:
            print(e)


    def cats_fixer(self, categories):
        bad = ["for", "and", "a", "other", "or", "of", "excl", "the", "not", "as", "&", "a"]
        cats = []
        good = []

        for cat in categories:
            cat = cat.split(" ")
            for c in cat: cats.append(c)

        for cat in cats:
            if cat not in bad:
                good.append(cat)

        return good


    def checker(self, keyword, categories: list):
        good = 0
        bad = 0
        cats = self.cats_fixer(categories)
        for category in cats:
            if good == (len(keyword) if len(keyword) < 5 else 5):
                return True

            if category in keyword:
                good += 1
            else:
                bad += 1
            print(good, bad, category)



    def scrape(self, soup, keyword):
        try:
            ul = soup.find("ul", {'class': "srp-results srp-list clearfix"})
            if ul is None: 
                self.stop = True
                return
            for i in range(1, 200):
                box = ul.find('li', {'data-view': f"mi:1686|iid:{i}"})
                url = box.find('a', {'class': "s-item__link"}, href=True)
                print(url["href"])
                self.page_scrape(url["href"], keyword)
                return

        except AttributeError as e:
            print(e)
        except Exception as e:
            print(e)
        
    
    def page_scrape(self, page, keyword):
        categories = []
        req = requests.get(page, headers=self.headers)
        soup = BeautifulSoup(req.text, 'lxml')
        table = soup.find("ul", {"aria-label": "Listed in category:"})
        categories = table.find_all("li", {"itemprop": "itemListElement"})
        for category in categories:
            cat = category.find("span")
            print(cat.text)
            categories.append(cat.text)
            


Searcher().get_keywords()