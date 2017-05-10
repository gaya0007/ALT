from DataDownloader import *
import datetime


start_date = datetime.date(2012,2,1)
end_date = datetime.date(2012,2,25)
download_historical_data('EUR_USD', start_date, end_date)