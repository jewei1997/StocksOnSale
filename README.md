Has been succesfully deployed to: https://stocks-on-sale.herokuapp.com/

## Other stats to add:
 - forward PE
 - divident yield
 - price to sales ratio
 - market cap
 - cash and cash equivalents
 - current assets
 - current liabilities
 - 1 month, 3 month, 1 year, 5 year (if it has) performance
 - price to book ratio

## Stretch stats
 - sector/industry
 - news
 
## Development
 - run `python manage.py runserver` to start the app locally
 - if you make changes to the frontend, run `npm run build && python manage.py runserver`
 - To update financial data in db, look at instructions in `update_financial_data.py`
 - To deploy to heroku, run: 
    - `git push heroku master`
    - remember heroku has its own postgres db, so you need to repopulate db
    - run `heroku run bash` to access heroku server
    - NOTE: heroku automatically runs any migrations
    
## Thoughts/Ideas
 - instead of doing search, for MVP would make more sense to just have 3 buttons for S&P500, NASDAQ, and DOW and the product would still be useful
 - all tickers: https://cloud.iexapis.com/stable/ref-data/symbols?token=pk_f73bd1961cb24068b2e354b45d1e5ac8
