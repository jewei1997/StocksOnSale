from rest_framework.views import APIView
from rest_framework.response import Response
from stocks.models import Stock


# Create your views here.
class PeRatios(APIView):
    """
    List all stocks with PE ratios sorted by PE ratio
    """

    def get_pe(self, ticker):
        try:
            pe = Stock.objects.get(ticker=ticker).pe_ratio
        except:
            return float("nan")
        return pe

    def get(self, request, format=None):
        stocks = Stock.objects.all()
        tickers = [stock.ticker for stock in stocks]
        pe_ratios = [(ticker, self.get_pe(ticker)) for ticker in tickers if self.get_pe(ticker)]
        sorted_by_pe = sorted(pe_ratios, key=lambda ticker_pe_tuple: ticker_pe_tuple[1])
        sorted_ticker_pe_data = {"tickers": [ticker_pe_tuple[0] for ticker_pe_tuple in sorted_by_pe],
                                 "pe_ratios": [ticker_pe_tuple[1] for ticker_pe_tuple in sorted_by_pe]}
        return Response(sorted_ticker_pe_data)
