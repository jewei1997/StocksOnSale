#from stocks.models import Stock
import requests


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


def main():
    sp500 = scrape_slick_charts_html("slick_charts_sp500.txt")
    dow = scrape_slick_charts_html("slick_charts_dow.txt")
    nasdaq = scrape_slick_charts_html("slick_charts_nasdaq.txt")

    print(sp500)
    print(len(sp500))
    print(dow)
    print(len(dow))
    print(nasdaq)
    print(len(nasdaq))



if __name__ == "__main__" or __name__ == "builtins":  # "builtins" is for running this in python prompt
    main()
