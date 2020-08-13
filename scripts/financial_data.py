import requests


class FinancialDataClient:

    IEX_CLOUD_API_KEY = 'pk_f73bd1961cb24068b2e354b45d1e5ac8'
    BATCH_LIMIT = 100

    def __init__(self):
        pass

    def _make_api_call_without_batching(self, tickers, requested_data):
        assert(len(tickers) <= self.BATCH_LIMIT and len(requested_data) <= self.BATCH_LIMIT)
        if not tickers or not requested_data:
            return {}
        api_call = 'https://cloud.iexapis.com/stable/stock/market/batch?symbols='
        api_call += ','.join(tickers)
        api_call += '&types='
        api_call += ','.join(requested_data)
        api_call += f'&token={self.IEX_CLOUD_API_KEY}'
        return requests.get(api_call).json()

    def _make_api_call_with_batching(self, tickers, requested_data):
        ticker_index = 0
        response = {}
        while ticker_index < len(tickers):
            ticker_batch = tickers[ticker_index: ticker_index + self.BATCH_LIMIT]
            api_result = self._make_api_call_without_batching(ticker_batch, requested_data)
            response.update(api_result)
            ticker_index += self.BATCH_LIMIT
        return response

    def _get_quotes(self, tickers):
        return self._make_api_call_with_batching(tickers, ["quote"])

    def get_pe_ratios(self, tickers):
        pe_ratios = []
        resp = self._get_quotes(tickers)
        for ticker in tickers:
            try:
                pe = resp[ticker]["quote"]["peRatio"]
            except:
                pe = None
            pe_ratios.append(pe)
        return pe_ratios

