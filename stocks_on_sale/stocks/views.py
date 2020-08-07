from rest_framework.views import APIView
from rest_framework.response import Response
from stocks.models import Stock
import requests
from bs4 import BeautifulSoup
import time


# Create your views here.
class PeRatios(APIView):
    """
    List all stocks with PE ratios sorted by PE ratio
    """

    count = 0

    def get_pe(self, ticker):
        if self.count > 0 and self.count % 3 == 0:
            print("Sleeping for 5 seconds")
            time.sleep(5)
        self.count += 1
        yhoo_finance_html = requests.get('https://finance.yahoo.com/quote/' + ticker)
        soup = BeautifulSoup(yhoo_finance_html.content)
        try:
            pe_span = soup.find_all("td", attrs={"data-test": "PE_RATIO-value"})[0]
        except:
            print(f"Unable to get pe ratio for {ticker}")
            return float("nan")
        try:
            pe = float(pe_span.contents[0].contents[0])
        except:
            print(f"{ticker} has pe ratio of NA")
            return float("nan")
        print(f"{self.count}: {ticker} - {pe}")
        return pe

    def get(self, request, format=None):
        stocks = Stock.objects.all()
        tickers = [stock.ticker for stock in stocks]
        pe_ratios = [(ticker, self.get_pe(ticker)) for ticker in tickers]
        sorted_by_pe = sorted(pe_ratios, key=lambda ticker_pe_tuple: ticker_pe_tuple[1])
        sorted_ticker_pe_data = {"tickers": [], "pe_ratios": []}
        sorted_ticker_pe_data["tickers"] = [ticker_pe_tuple[0] for ticker_pe_tuple in sorted_by_pe]
        sorted_ticker_pe_data["pe_ratios"] = [ticker_pe_tuple[1] for ticker_pe_tuple in sorted_by_pe]
        return Response(sorted_ticker_pe_data)
