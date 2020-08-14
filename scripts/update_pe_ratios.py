from stocks.models import Stock
from scripts.financial_data import FinancialDataClient, FinInfo

client = FinancialDataClient()
stocks = Stock.objects.all()
tickers = [stock.ticker for stock in stocks]
n = len(tickers)
info = client.get_info(tickers, [FinInfo.PE_RATIO, FinInfo.MARKET_CAP])
pe_ratios = info[0]
market_caps = info[1]
print(pe_ratios)
print(market_caps)
assert(len(pe_ratios) == n and len(market_caps) == n)
for i in range(n):
    ticker = tickers[i]
    pe = pe_ratios[i]
    market_cap = market_caps[i]
    # save new pe into db
    if not pe or not market_cap:
        continue
    s = Stock.objects.get(ticker=ticker)
    s.pe_ratio = pe
    s.market_cap = market_cap
    print(f"Saving Stock {s} into db")
    s.save()


