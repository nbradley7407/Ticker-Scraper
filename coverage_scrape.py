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

# initiate driver
service = Service('chromedriver.exe')
service.start()
driver = webdriver.Remote(service.service_url)
wait = WebDriverWait(driver, 60.0)


def get_title(element):
    title_element = element.find_element(By.XPATH, "//*[@id=\"rso\"]/div/div/div[1]/div/div/a/div/div[2]/div[2]")
    title = title_element.get_attribute("innerHTML")
    return title


def get_url(element):
    url_string = element.get_attribute('href')
    return url_string


def get_date(element):
    date_element = element.find_element(By.XPATH, "//*[@id=\"rso\"]/div/div/div[1]/div/div/a/div/div[2]/div[4]")
    date = date_element.get_attribute("innerHTML")
    return date


def scrape_info():
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "iRPxbe")))
    article_info = driver.find_elements(By.CLASS_NAME, "iRPxbe")
    return article_info[:3]

def scrape_urls():
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "WlydOe")))
    article_urls = driver.find_elements(By.CLASS_NAME, "WlydOe")
    return article_urls[:3]


with open('summaries.txt', 'w') as f:     # clear the text file
    f.close()


with open('summaries.txt', 'a') as f:     # main
    for i in my_tickers:
        driver.get(f'https://www.google.com/search?q={i}+stock&hl=en&tbm'
                   f'=nws&source=lnt&tbs=sbd:1&sa=X&ved=2ahUKEwitoYTL16n9AhVNP'
                   f'n0KHbyMBE4QpwV6BAgBECE&biw=2067&bih=2007&dpr=1')
        f.write(f'{i}\n')
        url_element = scrape_urls()
        info_element = scrape_info()
        for url, info in zip(url_element, info_element):
            f.write(f'{get_title(info)}\n')
            f.write(f'{get_date(info)}\n')
            f.write(f'{get_url(url)}\n')
        f.write('\n\n')
f.close()
