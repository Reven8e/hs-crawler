from bs4 import BeautifulSoup
import pandas as pd
import requests


def H_Instructor(where: int):
    url = "https://www.tariffnumber.com/2021/{0}"
    headers = headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"}

    r = requests.get(url.format(where), headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    table = soup.find("div", {"class": "col-md-9 col-12"})
    cols = table.find_all("div", {"class": 'mb-4 shadow'})
    for col in cols:
        title = col.find('div', {"class": 'rowheader'})




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
            g.append(k.replace("\n", "").replace("\r", "").replace(",", ""))
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

        self.df["HS Code"] = self.codes
        self.df["Description"] = self.desc
        self.df.to_csv("instructions.csv", index=False)



HS_Instructor(85).instructor() # Enter hs code number here
