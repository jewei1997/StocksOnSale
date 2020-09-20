from rest_framework.views import APIView
from rest_framework.response import Response
from stocks.models import Stock
from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse

import logging
import os

logger = logging.getLogger(__name__)


class PeRatios(APIView):
    """
    List all stocks with PE ratios sorted by PE ratio
    """

    def get(self, request, format=None):
        stocks = Stock.objects.all()
        pe_ratios = [(stock.ticker, stock.pe_ratio) for stock in stocks if stock.pe_ratio]
        sorted_by_pe = sorted(pe_ratios, key=lambda ticker_pe_tuple: ticker_pe_tuple[1])
        data = [{"ticker": ticker, "pe_ratio": pe} for (ticker, pe) in sorted_by_pe]
        return Response({"data": data})


class MarketCaps(APIView):
    """
    List all stocks with market caps sorted by market cap
    """

    def get(self, request, format=None):
        stocks = Stock.objects.all()
        market_caps = [(stock.ticker, stock.market_cap) for stock in stocks if stock.market_cap]
        sorted_by_market_cap = sorted(market_caps, key=lambda ticker_mc_tuple: ticker_mc_tuple[1])
        data = [{"ticker": ticker, "market_cap": mc} for (ticker, mc) in sorted_by_market_cap]
        return Response({"data": data})


class PercentageChange(APIView):
    """
    List all stocks with percentage change d days from today sorted by percentage change
    """

    class SupportedPeriod:
        WEEK = 7
        MONTH = 30
        YEAR = 365

    def _convert_days_to_supported_period(self, days):
        daysToSupportedPeriod = {7: self.SupportedPeriod.WEEK,
                                 30: self.SupportedPeriod.MONTH,
                                 365: self.SupportedPeriod.YEAR}
        return daysToSupportedPeriod[days]

    def check_float(self, num):
        return num and num != float('nan')

    def get(self, request, days, format=None):
        stocks = Stock.objects.all()
        supported_period = self._convert_days_to_supported_period(days)
        if supported_period == self.SupportedPeriod.WEEK:
            percentage_changes = [(stock.ticker, stock.one_week_percentage_change) for stock in stocks if self.check_float(stock.one_week_percentage_change)]
        elif supported_period == self.SupportedPeriod.MONTH:
            percentage_changes = [(stock.ticker, stock.one_month_percentage_change) for stock in stocks if self.check_float(stock.one_month_percentage_change)]
        elif supported_period == self.SupportedPeriod.YEAR:
            percentage_changes = [(stock.ticker, stock.one_year_percentage_change) for stock in stocks if self.check_float(stock.one_year_percentage_change)]
        else:
            raise Exception(f"Unsupported period {supported_period}")
        sorted_by_percentage_change = sorted(percentage_changes, key=lambda ticker_pc_tuple: ticker_pc_tuple[1])
        data = [{"ticker": ticker, "percentage_change": pc} for (ticker, pc) in sorted_by_percentage_change]
        return Response({"data": data})


class Dow(APIView):

    def get(self, request, format=None):
        stocks = Stock.objects.all()
        data = [{"ticker": stock.ticker, "dow": stock.is_in_dow} for stock in stocks]
        return Response({"data": data})


class Snp500(APIView):

    def get(self, request, format=None):
        stocks = Stock.objects.all()
        data = [{"ticker": stock.ticker, "snp500": stock.is_in_sp500} for stock in stocks]
        return Response({"data": data})


class Nasdaq(APIView):

    def get(self, request, format=None):
        stocks = Stock.objects.all()
        data = [{"ticker": stock.ticker, "nasdaq": stock.is_in_nasdaq} for stock in stocks]
        return Response({"data": data})


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
