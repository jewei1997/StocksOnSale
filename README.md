Has been succesfully deployed to: https://stocks-on-sale.herokuapp.com/

## Vision for the product
 - Maybe think about user use cases? 
 - Maybe we should do a formal write-up and share it with ppl
 - Use case 1: Create dashboards of stocks that is shareable with friends!
   - ex: Show Tesla vs Ford vs GM vs Toyota assets, liabilities, cash, pe ratios, etc.
   - shareable link (may not need to do accounts)
 - Use case 2: Create a dashboard of stocks that you're interested in and get news on them
   - Replace the mac sidebar stock thing you always look at and make the dashboard much better!
   - The problem this is solving is: I want to know what is going on with the stocks I am 
     tracking without visiting a bunch of websites to get news
 - Use case 3: Find stocks with specific stats (like fullstory)
   - need strong filtering criteria and lots of stats
   - ex: tech stocks 
 - Considerations:
   - MVP, what can we launch fast, get it in the hands of users, get feedback
   - what will people pay for? Prob shouldn't guess this -- do experiments
   - How do we differentiate our product with what is already out there?
   - Keep It Simple, Stupid
   - What is your competitive advantage as a business? 

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
 
## TODO (sorted in order of priority) (in progress):
 - [ ] Write up vision for product and share it with some friends
 - [ ] Redo the graph.
   - need column reordering and column resizing
 - [ ] More stats 
   - but which ones?
 
## Development
 - if you're just developing, just run: `npm run start`
 - to run the django backend that displays the frontend build: `npm run build && python manage.py runserver`
 - To update financial data in db, look at instructions in `update_financial_data.py`
 - To deploy to heroku, run: 
    - `git push heroku master`
    - remember heroku has its own postgres db, so you need to repopulate db
    - run `heroku run bash` to access heroku server
    - NOTE: heroku automatically runs any migrations as long as they're in the migrations/ folder
    
## Thoughts/Ideas for the future
 - [x] scrape s&p500, nasdaq, and dow all from one website: https://www.slickcharts.com/sp500
 - [x] instead of doing search, for MVP would make more sense to just have 3 buttons for S&P500, NASDAQ, and DOW and the product would still be useful
 
## IEXCloud Data ideas
 - all tickers: https://cloud.iexapis.com/stable/ref-data/symbols?token=pk_f73bd1961cb24068b2e354b45d1e5ac8
 - sectors that users can filter by: https://cloud.iexapis.com/stable/ref-data/sectors?token=pk_f73bd1961cb24068b2e354b45d1e5ac8
   - can use https://cloud.iexapis.com/stable/stock/market/collection/sector?collectionName=Technology&token=pk_f73bd1961cb24068b2e354b45d1e5ac8
     to see what stocks a sector has, but this endpoint actually isn't that good -- too much data
 - can also filter by tags https://cloud.iexapis.com/stable/stock/market/collection/tag?collectionName=Airlines&token=pk_f73bd1961cb24068b2e354b45d1e5ac8
   - also seems to have too much data
 - let's try: lists (mostactive, gainers, losers, iexvolume, iexpercent)
   - for example: https://cloud.iexapis.com/stable/stock/market/collection/list?collectionName=mostactive&token=pk_f73bd1961cb24068b2e354b45d1e5ac8
