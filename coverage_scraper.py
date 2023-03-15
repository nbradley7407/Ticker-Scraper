from requests_html import HTMLSession

my_tickers = ["AAPL",
              "AMZN",
              "ARRY",
              "ASLE",
              "ASML",
              "CCCS",
              "CVNA",
              "DCBO",
              "GOOG",
              "GOOGL",
              "HD",
              "INTA",
              "IWF",
              "MSFT",
              "NKE",
              "NVDA",
              "OI",
              "PERI",
              "PTON",
              "RBLX",
              "SMCI",
              "SMH",
              "SSNC",
              "TSLA",
              "TSM",
              ]


def main():
    with open('summaries.html', 'w') as f:     # clear the text file
        f.close()

    with open('summaries.html', 'a', encoding='utf-8') as f:     # main
        session = HTMLSession()
        for i in my_tickers:
            current_url = f'https://www.google.com/search?q={i}+stock&hl=en&tbm'\
                          f'=nws&source=lnt&tbs=sbd:1&sa=X&ved=2ahUKEwitoYTL16n9AhVNP'\
                          f'n0KHbyMBE4QpwV6BAgBECE&biw=2067&bih=2007&dpr=1'
            response = session.get(current_url)
            f.write('<br><br>'+('_'*150))
            f.write(f'<h1><p style="margin-left:50px";><a href="{current_url}"; style="color:green;">')
            f.write(f'{i}\n')
            f.write('</a></p></h1>')
            url_elements = response.html.find('.WlydOe')[:5]
            title_elements = response.html.find('.nDgy9d')[:5]
            blurb_elements = response.html.find('.nDgy9d')[:5]
            date_elements = response.html.find('.YsWzw')[:5]
            for url_element, title_element, blurb_element, date_element in zip(url_elements, title_elements, blurb_elements, date_elements):
                f.write(f'<h3 style="margin-left:50px"><a href="')
                f.write(f'{url_element.absolute_links.pop()}\n\n">')
                f.write(f'{title_element.text}\n')
                f.write(f'</a></h3><h4 style="margin-left:50px">')
                try:
                    f.write(f'{blurb_element.text}\n')
                except UnicodeEncodeError:
                    pass
                f.write(f'</h4>')
                f.write(f'<p style="margin-left:50px">{date_element.text}\n</p>')
            f.write('<br>')
        f.close()

    import webbrowser
    webbrowser.open('summaries.html')


if __name__ == "__main__":
    main()
