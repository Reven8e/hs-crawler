from selenium import webdriver, common
from secrets import passw
import pandas as pd


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
df = pd.read_csv("hs-codes.csv", names=["HS-Codes", "Keywords"])
codes = []
keywords = []

def scraper():
    driver.get("https://www.zauba.com/import-MACBOOK+AIR/hs-code-8471/p-1-hs-code.html")
    pages = driver.find_element_by_xpath('//*[@id="block-system-main"]/div[1]/div[3]/ul/li[2]/a')
    pages = int(pages.text)
    print(pages)
    for page in range(1, pages):
        driver.get(f"https://www.zauba.com/import-MACBOOK+AIR/hs-code-8471/p-{page}-hs-code.html")
        for i in range(2, 23):
            try:
                hs_code = driver.find_element_by_xpath(f'//*[@id="block-system-main"]/div[1]/div[3]/div[4]/div[2]/div/table/tbody/tr[{str(i)}]/td[2]/a')
                desc = driver.find_element_by_xpath(f'//*[@id="block-system-main"]/div[1]/div[3]/div[4]/div[2]/div/table/tbody/tr[{str(i)}]/td[3]')
                print(f"{hs_code.text}: {desc.text}")
                codes.append(hs_code.text)
                keywords.append(desc.text)

            except common.exceptions.NoSuchElementException:
                print(i)
                pass

    driver.close()


def login():
    driver.get('https://www.zauba.com/user/login')
    driver.find_element_by_name("name").send_keys("Bogan")
    driver.find_element_by_name("pass").send_keys(passw)
    try:
        equation = driver.find_element_by_xpath('//*[@id="user-login"]/div/div[3]/div')
        equation = equation.text
        print(equation)
        equation = equation.replace("Math question *", "")
        equation = equation.replace(" +", "")
        equation = equation.replace(" =", "")
        equation = equation.split(" ")
        print(type(equation))
        idk = int(equation[0]) + int(equation[1])
        print(idk)
        driver.find_element_by_id("edit-captcha-response").send_keys(str(idk))
    except Exception as e:
        print(e)

    driver.find_element_by_id("edit-submit").click()
    scraper()


login()


df["HS-Codes"] = codes
df["Keywords"] = keywords
df.drop_duplicates()
df.to_csv("hs-codes.csv")