from rest_framework.views import APIView
from rest_framework.response import Response
from stocks.models import Stock
from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse

import logging
import os


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


class FrontendAppView(View):
    """
    Serves the compiled frontend entry point (only works if you have run `yarn
    run build`).
    """
    def get(self, request):
        print (os.path.join(settings.REACT_APP_DIR, 'build', 'index.html'))
        try:
            with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            logging.exception('Production build of app not found')
            return HttpResponse(
                """
                This URL is only used when you have built the production
                version of the app. Visit http://localhost:3000/ instead, or
                run `yarn run build` to test the production version.
                """,
                status=501,
            )