from DataDownloader import *
import datetime


start_date = datetime.date(2014,1,1)
end_date = datetime.date(2017,6,25)
download_historical_data('EUR_USD', start_date, end_date)