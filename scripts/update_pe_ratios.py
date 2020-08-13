from stocks.models import Stock
from scripts.financial_data import FinancialDataClient

client = FinancialDataClient()
stocks = Stock.objects.all()
tickers = [stock.ticker for stock in stocks]
pe_ratios = client.get_pe_ratios(tickers)
for i in range(len(pe_ratios)):
    ticker = tickers[i]
    pe = pe_ratios[i]
    # save new pe into db
    if not pe:
        continue
    s = Stock.objects.get(ticker=ticker)
    s.pe_ratio = pe
    print(f"Saving Stock {s} into db")
    s.save()


