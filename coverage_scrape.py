import nltk
from newspaper import Article
from newspaper import ArticleException
import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

my_tickers = [
    "AAPL",
    "ADBE",
    "AMZN",
    "ARKK",
    "ASLE",
    "ASML",
    "CCCS",
    "CHWY",
    "CVNA",
    "DCBO",
    "F",
    "GOOGL",
    "HD",
    "INTA",
    "MBLY",
    "NKE",
    "NRDS",
    "PSTG",
    "PTON",
    "SMCI",
    "SMH",
    "SSNC",
    "TSLA",
    "TSM",
    "RBLX",
]


service = Service('chromedriver.exe')
service.start()
driver = webdriver.Remote(service.service_url)
wait = WebDriverWait(driver, 60.0)


def get_info(article):
    a = Article(article)
    try:
        a.download()
        a.parse()
        a.nlp()
        return f'Title: {a.title}',\
               f'Date: {a.publish_date}'
    except ArticleException:
        print(f"Error getting summary")


def get_title(element):

    title_element = element.find_element(By.XPATH, "//*[@id=\"rso\"]/div/div/div[1]/div/div/a/div/div[2]/div[2]")
    title = title_element.get_attribute("innerHTML")
    return title


def get_url(element):
    url = element.get_attribute('href')
    return url


def get_date(element):
    date_element = element.find_element(By.XPATH, "//*[@id=\"rso\"]/div/div/div[1]/div/div/a/div/div[2]/div[4]")
    date = date_element.get_attribute("innerHTML")
    return date


def scrape(ticker):
    driver.get(f'https://www.google.com/search?q={ticker}+stock&hl=en&tbm'
               f'=nws&source=lnt&tbs=sbd:1&sa=X&ved=2ahUKEwitoYTL16n9AhVNP'
               f'n0KHbyMBE4QpwV6BAgBECE&biw=2067&bih=2007&dpr=1')
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "WlydOe")))
    article_elements = driver.find_elements(By.CLASS_NAME, "WlydOe")
    return article_elements[:3]


with open('summaries.txt', 'w') as f:     # clear the text file
    f.close()


with open('summaries.txt', 'a') as f:
    for i in my_tickers:
        f.write(f'{i}\n')
        data = scrape(i)
        for element in data:
            f.write(f'{get_title(element)}\n')
            f.write(f'{get_date(element)}\n')
            f.write(f'{get_url(element)}\n')
        f.write('\n\n')
        #for url in urls:
            #f.write(f'{get_info(url)}\n')
            #f.write(f'{url}\n\n')
f.close()
