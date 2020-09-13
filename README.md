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
