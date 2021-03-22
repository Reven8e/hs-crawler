from googlesearch import search
import pandas as pd
import re


class Google:
    def __init__(self):
        self.csv = pd.read_csv("products.csv")
        self.products = [product for product in self.csv["Products"]]
        self.df = pd.DataFrame()
        self.hs_codes = []
        self.after_products = []
        self.good = 0


    def key_remover(self, og):
        key = re.sub(r'[^\w]', ' ', og)
        key = key.split(" ")
        while '' in key:
            key.remove('')
        return key

    def stripper(self, url):
        print(url)
        url = url.lower()
        url = url.replace("https://www.zauba.com/", "")
        url = url.split("/")
        keyword = url[0].replace("import-", "")
        keyword = keyword.split("+")
        if len(keyword) == 1: keyword = keyword[0].split("-")
        print(1, keyword)
        if len(url) > 1: return keyword, url[1]
        else: return keyword, False


    def find_hs(self, text):
        print(3, text)
        text = text.replace("hs-code-", "")
        text = text.replace("-hs-code.html", "")
        print(4, text)
        self.good += 1
        return text


    def checker(self, og_key, keywords, hidden_hs):
        good = 0
        bad = 0
        og = self.key_remover(og_key)
        print(1.5, og)
        for key in og:
            if good >= 2:
                self.after_products.append(og_key)
                self.hs_codes.append(self.find_hs(hidden_hs))
                break

            if key in keywords:
                print(2, key)
                good += 1
            else:
                bad += 1
                if bad == 2:
                    good = 0


    def main(self):
        i = 0
        for product in self.products[3:]:
            i+= 1
            if i == 30:
                break
            urls = search(product.lower() + " hs code")

            for url in urls:
                if "www.zauba.com" in url:
                    print("=================================")
                    url_keyword, hidden_hs = self.stripper(url)
                    if hidden_hs is False: continue
                    self.checker(product.lower(), url_keyword, hidden_hs)

        print(f"Ratio: {self.good}/{i}")
        self.df["HS Code(s)"] = self.hs_codes
        self.df["Products(s)"] = self.after_products
        self.df.to_csv("Final.csv", index=False)