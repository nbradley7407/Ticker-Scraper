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
    "PERI",
]

# initiate driver
service = Service('chromedriver.exe')
service.start()
driver = webdriver.Remote(service.service_url)
wait = WebDriverWait(driver, 60.0)


def get_title(element):
    title_string = element.get_attribute("innerHTML")
    return title_string


def get_url(element):
    url_string = element.get_attribute('href')
    return url_string


def get_blurb(element):
    blurb_string = element.get_attribute("innerHTML")
    return blurb_string


def get_date(element):
    date_string = element.get_attribute("innerHTML")
    return date_string


def scrape_dates():
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".OSrXXb.ZE0LJd.YsWzw")))
    article_dates = driver.find_elements(By.CSS_SELECTOR, ".OSrXXb.ZE0LJd.YsWzw")
    return article_dates[:3]


def scrape_blurb():
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".GI74Re.nDgy9d")))
    article_blurbs = driver.find_elements(By.CSS_SELECTOR, ".GI74Re.nDgy9d")
    return article_blurbs[:3]


def scrape_titles():
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".mCBkyc.ynAwRc.MBeuO.nDgy9d")))
    article_titles = driver.find_elements(By.CSS_SELECTOR, ".mCBkyc.ynAwRc.MBeuO.nDgy9d")
    return article_titles[:3]


def scrape_urls():
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "WlydOe")))
    article_urls = driver.find_elements(By.CLASS_NAME, "WlydOe")
    return article_urls[:3]


with open('summaries.html', 'w') as f:     # clear the text file
    f.close()

tab = '&nbsp&nbsp&nbsp&nbsp&nbsp'
with open('summaries.html', 'a') as f:     # main
    for i in my_tickers:
        driver.get(f'https://www.google.com/search?q={i}+stock&hl=en&tbm'
                   f'=nws&source=lnt&tbs=sbd:1&sa=X&ved=2ahUKEwitoYTL16n9AhVNP'
                   f'n0KHbyMBE4QpwV6BAgBECE&biw=2067&bih=2007&dpr=1')
        f.write('<br><br>'+('_'*150))
        f.write(f'<h1><p style="color:green;">{tab}')
        f.write(f'{i}\n')
        f.write('</p></h1>')
        url_element = scrape_urls()
        title_element = scrape_titles()
        blurb_element = scrape_blurb()
        date_element = scrape_dates()
        for url, title, blurb, date in zip(url_element, title_element, blurb_element, date_element):
            f.write(f'<h3>{tab}<a href="')
            f.write(f'{get_url(url)}\n\n')
            f.write('">')
            f.write(f'{get_title(title)}\n')
            f.write(f'</a></h3><h4>{tab}')
            f.write(f'{get_blurb(blurb)}\n')
            f.write(f'</h4>{tab}')
            f.write(f'{get_date(date)}\n')
        f.write('<br>')
    f.close()


