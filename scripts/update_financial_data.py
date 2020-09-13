from stocks.models import Stock
from scripts.financial_data import FinancialDataClient

"""
To run:
python manage.py shell
> exec(open("scripts/update_financial_data.py").read())

Tip:
When testing, change tickers = ["TSLA", "AMZN"]
"""

def main():
    client = FinancialDataClient()
    stocks = Stock.objects.all()
    tickers = [stock.ticker for stock in stocks]
    n = len(tickers)
    pe_ratios = client.get_pe_ratios(tickers)
    market_caps = client.get_market_caps(tickers)
    one_week_percentage_changes = client.get_price_percentage_change_from_today(tickers, 7)
    one_month_percentage_changes = client.get_price_percentage_change_from_today(tickers, 30)
    one_year_percentage_changes = client.get_price_percentage_change_from_today(tickers, 365)
    print(pe_ratios)
    print(market_caps)
    print(one_week_percentage_changes)
    print(one_month_percentage_changes)
    print(one_year_percentage_changes)
    assert(n == len(pe_ratios) == len(market_caps))
    assert(n == len(one_week_percentage_changes) == len(one_month_percentage_changes) == len(one_year_percentage_changes))
    for i in range(n):
        # save new pe into db
        if not pe_ratios[i] or not market_caps[i] or not one_week_percentage_changes[i] or not one_month_percentage_changes[i] or not one_year_percentage_changes[i]:
            continue
        s = Stock.objects.get(ticker=tickers[i])
        s.pe_ratio = pe_ratios[i]
        s.market_cap = market_caps[i]
        s.one_week_percentage_change = one_week_percentage_changes[i]
        s.one_month_percentage_change = one_month_percentage_changes[i]
        s.one_year_percentage_change = one_year_percentage_changes[i]
        print(f"Saving Stock {s} into db")
        s.save()


if __name__ == "__main__" or __name__ == "builtins":  # "builtins" is for running this in python prompt
    main()
