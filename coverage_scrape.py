import selenium
import nltk
from newspaper import Article
import 

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


def get_summary(article):
    a = Article(article)
    a.download()
    a.parse()
    a.nlp()
    print(a.summary)

def scrape_sa(ticker):


for i in my_tickers:
