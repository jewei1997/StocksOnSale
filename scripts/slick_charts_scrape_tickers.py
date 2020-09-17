from stocks.models import Stock

"""
Use this script to scrape tickers from slick_charts*.txt files in scripts/
that belong to s&p500, dow, and nasdaq. It marks the tickers that are in those
indicies as such in the database.

To run:
python manage.py shell
> exec(open("scripts/slick_charts_scrape_tickers.py").read())
"""

def scrape_slick_charts_html(_file):
    with open("scripts/" + _file, 'r') as reader:
        line = reader.readline()
        tickers = set()
        while line != '':
            line = reader.readline()
            if "/symbol/" in line:
                symbol_idx = line.find("/symbol/")+len("/symbol/")
                line = line[symbol_idx:]
                end = line.find("\"")
                ticker = line[:end]
                tickers.add(ticker)
    return tickers


def get_stock_object(ticker):
    try:
        s = Stock.objects.get(ticker=ticker)
    except:
        s = Stock(ticker=ticker)
    return s


def mark_as_in_sp500(tickers):
    for ticker in tickers:
        s = get_stock_object(ticker)
        s.is_in_sp500 = True
        print(f"Saving stock {s} marked as in sp500 in db")
        s.save()


def mark_as_in_dow(tickers):
    for ticker in tickers:
        s = get_stock_object(ticker)
        s.is_in_dow = True
        print(f"Saving stock {s} marked as in dow in db")
        s.save()


def mark_as_in_nasdaq(tickers):
    for ticker in tickers:
        s = get_stock_object(ticker)
        s.is_in_nasdaq = True
        print(f"Saving stock {s} marked as in nasdaq in db")
        s.save()


def main():
    sp500 = scrape_slick_charts_html("slick_charts_sp500.txt")
    dow = scrape_slick_charts_html("slick_charts_dow.txt")
    nasdaq = scrape_slick_charts_html("slick_charts_nasdaq.txt")

    mark_as_in_sp500(sp500)
    mark_as_in_dow(dow)
    mark_as_in_nasdaq(nasdaq)


if __name__ == "__main__" or __name__ == "builtins":  # "builtins" is for running this in python prompt
    main()
