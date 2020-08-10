import requests
from bs4 import BeautifulSoup
import time
from stocks.models import Stock

count = 0


def get_pe(ticker):
    global count
    if count > 0 and count % 3 == 0:
        print("Sleeping for 5 seconds")
        time.sleep(5)
    count += 1
    yhoo_finance_html = requests.get('https://finance.yahoo.com/quote/' + ticker)
    soup = BeautifulSoup(yhoo_finance_html.content)
    try:
        pe_span = soup.find_all("td", attrs={"data-test": "PE_RATIO-value"})[0]
    except:
        print(f"Unable to get pe ratio for {ticker}")
        return None
    try:
        pe = float(pe_span.contents[0].contents[0])
    except:
        print(f"{ticker} has pe ratio of NA")
        return None
    print(f"{count}: {ticker} - {pe}")
    return pe


stocks = Stock.objects.all()
tickers = [stock.ticker for stock in stocks]
for ticker in tickers:
    pe = get_pe(ticker)
    # save new pe into db
    if not pe:
        continue
    s = Stock.objects.get(ticker=ticker)
    s.pe_ratio = pe
    print(f"Saving Stock {s} into db")
    s.save()


