from stocks.models import Stock
from scripts.financial_data import FinancialDataClient, FinInfo

"""
To run:
python manage.py shell
> exec(open("scripts/update_pe_ratios.py").read())

Tip:
When testing, change tickers = ["AMZN"]
"""

def main():
    client = FinancialDataClient()
    stocks = Stock.objects.all()
    tickers = [stock.ticker for stock in stocks]
    n = len(tickers)
    info = client.get_info(tickers, [
        FinInfo.PE_RATIO,
        FinInfo.MARKET_CAP,
        FinInfo.ONE_WEEK_CHANGE,
        FinInfo.ONE_MONTH_CHANGE,
        FinInfo.ONE_YEAR_CHANGE,
    ])
    pe_ratios = info[0]
    market_caps = info[1]
    one_week_percentage_changes = info[2]
    one_month_percentage_changes = info[3]
    one_year_percentage_changes = info[4]
    print(pe_ratios)
    print(market_caps)
    print(one_week_percentage_changes)
    print(one_month_percentage_changes)
    print(one_year_percentage_changes)
    assert(n == len(pe_ratios) == len(market_caps))
    assert(n == len(one_week_percentage_changes) == len(one_month_percentage_changes) == len(one_year_percentage_changes))
    for i in range(n):
        ticker = tickers[i]
        pe = pe_ratios[i]
        market_cap = market_caps[i]
        one_week_percentage_change = one_week_percentage_changes[i]
        one_month_percentage_change = one_month_percentage_changes[i]
        one_year_percentage_change = one_year_percentage_changes[i]
        # save new pe into db
        if not pe or not market_cap or not one_week_percentage_change or not one_month_percentage_change or not one_year_percentage_change:
            continue
        s = Stock.objects.get(ticker=ticker)
        s.pe_ratio = pe
        s.market_cap = market_cap
        s.one_week_percentage_change = one_week_percentage_change
        s.one_month_percentage_change = one_month_percentage_change
        s.one_year_percentage_change = one_year_percentage_change
        print(f"Saving Stock {s} into db")
        s.save()


if __name__ == "__main__" or __name__ == "builtins":
    main()
