import requests
import datetime
from datetime import date
import logging

logger = logging.getLogger(__name__)

class FinancialDataClient:

    IEX_CLOUD_API_KEY = 'pk_f73bd1961cb24068b2e354b45d1e5ac8'
    BATCH_LIMIT = 100

    def __init__(self):
        pass

    ############################################################
    ############## Financial stat getters ######################
    ############################################################

    def get_pe_ratios(self, tickers):
        resp = self._get_api_quotes_endpoint(tickers)
        return [resp[ticker]["quote"]["peRatio"] for ticker in tickers]

    def get_market_caps(self, tickers):
        resp = self._get_api_quotes_endpoint(tickers)
        return [resp[ticker]["quote"]["marketCap"] for ticker in tickers]

    def get_price_percentage_change_from_today(self, tickers, day_diff):
        adjusted_date_today = self._adjust_date(date.today())
        adjusted_past_date = self._adjust_date(date.today() - datetime.timedelta(days=day_diff))

        resp_past_date = self._get_historial_prices_endpoint(tickers, adjusted_past_date)
        resp_today = self._get_historial_prices_endpoint(tickers, adjusted_date_today)

        past_prices = self._extract_closing_prices_from_api_response(resp_past_date)
        current_prices = self._extract_closing_prices_from_api_response(resp_today)

        return self._calculate_percentage_changes(tickers, past_prices, current_prices)

    ############################################################
    ############## API endpoint handlers #######################
    ############################################################

    def _get_api_quotes_endpoint(self, tickers):
        ticker_index = 0
        response = {}
        while ticker_index < len(tickers):
            ticker_batch = tickers[ticker_index: ticker_index + self.BATCH_LIMIT]
            api_result = self._get_api_quotes_endpoint_helper(ticker_batch)
            response.update(api_result)
            ticker_index += self.BATCH_LIMIT
        return response

    def _get_api_quotes_endpoint_helper(self, tickers):
        # example call: https://cloud.iexapis.com/stable/stock/aapl/batch?types=quote&token=pk_f73bd1961cb24068b2e354b45d1e5ac8
        assert(len(tickers) <= self.BATCH_LIMIT)
        if not tickers:
            return {}

        # build api call and make get request
        api_call = 'https://cloud.iexapis.com/stable/stock/market/batch?symbols='
        api_call += ','.join(tickers)
        api_call += '&types='
        api_call += 'quote'
        api_call += f'&token={self.IEX_CLOUD_API_KEY}'
        return requests.get(api_call).json()

    def _get_historial_prices_endpoint(self, tickers, _date):
        ticker_index = 0
        response = []
        while ticker_index < len(tickers):
            ticker_batch = tickers[ticker_index: ticker_index + self.BATCH_LIMIT]
            api_result = self._get_historial_prices_endpoint_helper(ticker_batch, _date)
            response.extend(api_result)
            ticker_index += self.BATCH_LIMIT
        return response

    def _get_historial_prices_endpoint_helper(self, tickers, _date):
        # example call: https://cloud.iexapis.com/stable/stock/market/chart/date/20200820?symbols=tsla,aapl&chartByDay=true&token=pk_f73bd1961cb24068b2e354b45d1e5ac8
        assert(len(tickers) <= self.BATCH_LIMIT)
        if not tickers:
            return {}

        # convert datetime object to correctly formatted string
        splitted_date = str(_date).split('-')
        date_no_spaces = ''.join(splitted_date)

        # build api call and make get request
        api_call = 'https://cloud.iexapis.com/stable/stock/market/chart/date/'
        api_call += date_no_spaces
        api_call += '?symbols='
        api_call += ','.join(tickers)
        api_call += '&chartByDay=true'
        api_call += f'&token={self.IEX_CLOUD_API_KEY}'
        return requests.get(api_call).json()

    ############################################################
    ############## helper functions ############################
    ############################################################

    def _adjust_date(self, _date):
        """
        Adjust the date to the nearest date in the past that has data. For example, if the stock market hasn't
        opened yet on the date, adjust to the day before. If it is a weekend, adjust to the nearest Friday.
        """
        if _date == date.today():
            _date = _date - datetime.timedelta(days=1)
        if _date.weekday() == 5:  # saturday
            _date = _date - datetime.timedelta(days=1)
        if _date.weekday() == 6:
            _date = _date - datetime.timedelta(days=2)
        return _date

    def _extract_closing_prices_from_api_response(self, resp):
        prices = []
        for stock_arr in resp:
            if len(stock_arr) == 0:
                prices.append(0)
                continue
            stock_dict = stock_arr[0]
            prices.append(stock_dict["uClose"])
        return prices

    def _calculate_percentage_changes(self, tickers, past_prices, current_prices):
        assert(len(tickers) == len(past_prices) == len(current_prices))
        percentage_changes = []
        for i in range(len(past_prices)):
            if not past_prices[i] or not current_prices[i]:
                logger.warning(f"No percentage change retrieved for ticker {ticker}")
                percentage_changes.append(float('nan'))  # when unable to get value
                continue
            percentage_changes.append((current_prices[i] - past_prices[i])/past_prices[i])
        return percentage_changes

