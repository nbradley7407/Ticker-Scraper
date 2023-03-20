from requests_html import HTMLSession
import os

TICKER_FILE = 'tickers.txt'


def get_tickers():
    if not os.path.isfile(TICKER_FILE):
        return []
    with open(TICKER_FILE, 'r') as f:
        return [line.strip() for line in f.readlines()]


def save_tickers(tickers):
    with open(TICKER_FILE, 'w') as f:
        f.write('\n'.join(tickers))


def clear_tickers():
    with open("tickers.txt", "w") as f:
        f.write("")
    print("Tickers file cleared.")


def main():
    # prompt the user for input of num_articles
    num_articles = int(input("Enter the number of articles to retrieve for each ticker: "))

    # prompt the user for input of tickers
    my_tickers = get_tickers()
    while True:
        action = input("1) What would you like to do? ('r' to run, 'e' to edit ticker list): ")

        if action.lower() == 'e':
            while True:
                sub_action = input("2) Would you like to add or delete tickers? "
                                   "('p' to show list, 'a' to add, 'd' to delete, 'c' to clear, 's' to save): ")

                if sub_action.lower() == 's':
                    save_tickers(my_tickers)
                    print(f"{len(my_tickers)} tickers in '{TICKER_FILE}'")
                    break

                elif sub_action.lower() == 'a':
                    while True:
                        ticker = input("3) Enter ticker to add (or 'q' to quit): ").upper()
                        if ticker == 'Q':
                            break
                        elif ticker in my_tickers:
                            print(f"{ticker} is already in your list")
                        else:
                            my_tickers.append(ticker)

                elif sub_action.lower() == 'd':
                    while True:
                        ticker = input("3) Enter ticker to delete (or 'q' to quit): ").upper()
                        if ticker == 'Q':
                            break
                        if ticker in my_tickers:
                            my_tickers.remove(ticker)
                        else:
                            print(f"Ticker '{ticker}' not found in list")

                elif sub_action.lower() == 'c':
                    my_tickers = []
                    print("Ticker list cleared")

                elif sub_action.lower() == 'p':
                    print(list(my_tickers))

                else:
                    print("Invalid input")

        elif action.lower() == 'r':
            break

    with open('summaries.html', 'w', encoding='utf-8') as f:     # main
        session = HTMLSession()
        for i in my_tickers:
            current_url = f'https://www.google.com/search?q={i}+stock&hl=en&tbm'\
                          f'=nws&source=lnt&tbs=sbd:1&sa=X&ved=2ahUKEwitoYTL16n9AhVNP'\
                          f'n0KHbyMBE4QpwV6BAgBECE&biw=2067&bih=2007&dpr=1'
            response = session.get(current_url)
            f.write(f'<br><br>{"_" * 150}')
            f.write(f'<h1><p style="margin-left:50px";><a href="{current_url}"; style="color:green;">')
            f.write(f'{i}\n')
            f.write('</a></p></h1>')
            url_elements = response.html.find('.WlydOe')[:num_articles]
            title_elements = response.html.find('.mCBkyc.ynAwRc.MBeuO.nDgy9d')[:num_articles]
            blurb_elements = response.html.find('.GI74Re.nDgy9d')[:num_articles]
            date_elements = response.html.find('.YsWzw')[:num_articles]
            for url_element, title_element, blurb_element, date_element in zip(url_elements, title_elements,
                                                                               blurb_elements, date_elements):
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

    os.startfile('summaries.html')


if __name__ == "__main__":
    main()
