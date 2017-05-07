import DataDownloader
import datetime


start_date = datetime.date(2017,4,10)
end_date = datetime.date(2017,4,30)
download_historical_data('EUR_USD', start_date, end_date)
parse_csv('./Data/EUR_USD_Week4.csv')