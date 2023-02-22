import nltk
from newspaper import Article
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
    "GOOG",
    "GOOGL",
    "HD",
    "INTA",
    "MBLY",
    "NKE",
    "NRDS",
    "PSTG",
    "PTON",
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


def get_summary(article):
    a = Article(article)
    a.download()
    a.parse()
    a.nlp()
    return a.text, a.summary, a.publish_date




def scrape_sa(ticker):
    driver.get(f'https://www.google.com/search?q={ticker}+stock&hl=en&tbm'
               f'=nws&source=lnt&tbs=sbd:1&sa=X&ved=2ahUKEwitoYTL16n9AhVNP'
               f'n0KHbyMBE4QpwV6BAgBECE&biw=2067&bih=2007&dpr=1')
    first_article = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "WlydOe")))
    article_url = first_article.get_attribute('href')
    return article_url


with open('summaries.txt', 'w') as f:     # clear the text file
    f.close()


for i in my_tickers:
    url = scrape_sa(i)
    summary = get_summary(url)
    with open('summaries.txt', 'a') as f:
        f.write(f'{i}\n')
        f.write(f'{summary}\n\n')
    time.sleep(2)
f.close()
