from DataDownloader import *
from test_data import*
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import os

def download_data_and_resample(start_date, end_date):
	start_date = datetime.date(2014,1,1)
	end_date = datetime.date(2017,6,25)
	download_historical_data('EUR_USD', start_date, end_date)
	
def plot_data(pair, period, start_date, end_date):
	wmp = week_of_month(start_date)
	file_list = []
	print os.getcwd()
	for single_date in date_range(start_date, end_date):
		wm = week_of_month(single_date)
		if wm != wmp and wm != 0:
			wmp = wm
			path = "Data/" + single_date.strftime('%Y') + '_' + single_date.strftime('%m') + '_' + pair + "_Week{}".format(wmp) + '/' + pair + "_Week{}".format(wmp)+ ".csv-" + period +"_OHLC.pkl" 
			if os.path.exists(path):
				file_list.append(path)
			else:
				print "couldn't find file {}".format(path)
	df_list = [pd.read_pickle(file) for file in file_list]
	df = pd.concat(df_list)
	df['RateBid']['high'].plot()
	plt.legend()
	plt.show()

plot_data("EUR_USD", "1D", datetime.date(2014,1,1), datetime.date(2017,6,25))