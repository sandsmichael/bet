import pandas as pd 
import pandas_market_calendars as mcal

# pro: convencience
# con: all scripts need to be triggered by a function call 

def today_business_day_number(date:int = None):
    #awa_dates
    return bool(len(pd.bdate_range(date, date)))

def today_market_day_number(date:int = None):
    #awa_dates
    start_date='2012-07-01'
    end_date='2012-07-10'
    nyse = mcal.get_calendar('NYSE')
    early = nyse.schedule(start_date='2012-07-01', end_date='2012-07-10')

def business_day_schedule(*args, **kwargs):
    def run(func):
        if kwargs.get('bd_run_day') == 9:
            # do something                          # check the mainframe if not already run
            func()                                  # call the function
            #pass                                   # update awa status log
        else:
            print('not the desired business day - will not run')
    return run # return the inner function


@business_day_schedule(bd_run_number=11)
def init():
    print('rrrrrun')
    # ... automated job goes here or this function calls it somewhere else... #

