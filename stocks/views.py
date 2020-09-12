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

    def get_pe(self, ticker):
        try:
            pe = Stock.objects.get(ticker=ticker).pe_ratio
        except:
            logger.warning(f"Unable to find pe ratio for ticker {ticker}, using float('nan') instead")
            return float("nan")
        return pe

    def get(self, request, format=None):
        stocks = Stock.objects.all()
        tickers = [stock.ticker for stock in stocks]
        pe_ratios = [(ticker, self.get_pe(ticker)) for ticker in tickers if self.get_pe(ticker)]
        sorted_by_pe = sorted(pe_ratios, key=lambda ticker_pe_tuple: ticker_pe_tuple[1])
        data = [{"ticker": ticker, "pe_ratio": pe} for (ticker, pe) in sorted_by_pe]
        return Response({"data": data})


class MarketCaps(APIView):
    """
    List all stocks with market caps sorted by market cap
    """

    def get_market_cap(self, ticker):
        try:
            market_cap = Stock.objects.get(ticker=ticker).market_cap
        except:
            logger.warning(f"Unable to find market cap for ticker {ticker}, using 0 instead")
            return 0
        return market_cap

    def get(self, request, format=None):
        stocks = Stock.objects.all()
        tickers = [stock.ticker for stock in stocks]
        market_caps = [(ticker, self.get_market_cap(ticker)) for ticker in tickers if self.get_market_cap(ticker)]
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

    def _get_percentage_change(self, ticker, supported_period):
        percentage_change = 0
        try:
            if supported_period == self.SupportedPeriod.WEEK:
                percentage_change = Stock.objects.get(ticker=ticker).one_week_percentage_change
            elif supported_period == self.SupportedPeriod.MONTH:
                percentage_change = Stock.objects.get(ticker=ticker).one_month_percentage_change
            elif supported_period == self.SupportedPeriod.YEAR:
                percentage_change = Stock.objects.get(ticker=ticker).one_year_percentage_change
            else:
                raise Exception(f"Unsupported period {supported_period}")
        except Exception as e:
            logger.warning(f"Unable to get percentage change for period of {supported_period} days for ticker {ticker}"
                           f", using float('nan') instead")
            logger.warning(e)
            percentage_change = float('nan')
        return percentage_change

    def _convert_days_to_supported_period(self, days):
        daysToSupportedPeriod = {7: self.SupportedPeriod.WEEK,
                                 30: self.SupportedPeriod.MONTH,
                                 365: self.SupportedPeriod.YEAR}
        return daysToSupportedPeriod[days]

    def get(self, request, days, format=None):
        stocks = Stock.objects.all()
        tickers = [stock.ticker for stock in stocks]
        supported_period = self._convert_days_to_supported_period(days)
        percentage_changes = [
                                (ticker, self._get_percentage_change(ticker, supported_period))
                                for ticker in tickers
                                if self._get_percentage_change(ticker, supported_period)
                             ]
        sorted_by_percentage_change = sorted(percentage_changes, key=lambda ticker_pc_tuple: ticker_pc_tuple[1])
        data = [{"ticker": ticker, "percentage_change": pc} for (ticker, pc) in sorted_by_percentage_change]
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
