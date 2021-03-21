from bs4 import BeautifulSoup
import requests, json


class crawl:
    def __init__(self, keyword):
        self.url = f"https://www.zauba.com/import-{keyword}"
        self.pages = 0
        self.user = "Bogan"
        self.password = "fwqfqwf@F"


    def login(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
            'referer':'https://www.google.com/'
        }
        data = json.dumps({
            "name": self.user,
            "pass": self.password,
            "form_build_id": "form-qJTO689eBI7qFs9s57x2ZTyD2LWqq7qIDWRE2L_4gV0",
            "form_id": "user_login",
            "captcha_sid": "16854664",
            "captcha_token": None,
            "captcha_response": 8,
            "op": "Log+in"
        })

        req = requests.post("https://www.zauba.com/user/login", data=data, headers=headers)
        if "The answer you entered for the CAPTCHA" in req.text:
            print("rip captcha")
        elif "Sorry, unrecognized username" in req.text:
            print("username isnt correct yay")
        else:
            print(req.text)


    def finder(self, page):
        req = requests.get(self.url+f"/p-{page}-hs-code.html")
        soup = BeautifulSoup(req.text, "lxml")
        ul = soup.find
        tbody = soup.find("tbody")
        tr = tbody.find_all("tr")
        tr.remove(tr[0])

        for t in tr:
            try:
                td = t.find_all("td")
                desc = t.find("td", {"class": "desc"})
                hs_code = td[1].find("a")
                print(hs_code.text, desc.text)
            except IndexError:
                pass

    
    def looper(self):
        req = requests.get(self.url+"-hs-code.html")
        soup = BeautifulSoup(req.text, "lxml")
        ul = soup.find("ul", {"class": "pager"})
        li = ul.find("li", {"class": "pager-item"})
        a = li.find("a")
        self.pages = int(a.text)

        for i in range(1, self.pages):
            self.finder(i)

crawl("apple-macbook").login()

# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
#     'referer':'https://www.google.com/', 
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "accept-encoding": "gzip, deflate, br"
# }

# data = json.dumps ({
#     "q": "apple macbook hs code",
#     "oq": "apple ma",
#     "ie": "UTF-8",
#     "sourceid": "chrome",
#     "aqs": "chrome.0.69i59j0i20i263j69i57j0i131i433j0j69i60j69i61j69i60.1676j0j9"
# })

# r = requests.get("https://www.google.com/search?q=apple+macbook+hs+code", headers=headers, data=data)
# print(r.text)