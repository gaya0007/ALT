from DataDownloader import *
from test_data import*
import datetime
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib import style
import pandas as pd
import os
from analysis_funcs import*

style.use('ggplot')

def download_data_and_resample(pair, start_date, end_date):
	download_historical_data(pair, start_date, end_date)
	
def create_dataframe(pair, period, start_date, end_date):
	wmp = week_of_month(start_date)
	file_list = []
	print os.getcwd()
	for single_date in date_range(start_date, end_date):
		wm = week_of_month(single_date)
		if wm != wmp and wm != 0:
			wmp = wm
			path = "Data/" + single_date.strftime('%Y') + '_' + single_date.strftime('%m') + '_' + pair + "_Week{}".format(wmp) + '/' + pair + "_Week{}".format(wmp)+ ".csv-1Min" + "_OHLC.pkl" 
			if os.path.exists(path):
				file_list.append(path)
			else:
				print "couldn't find file {}".format(path)
	df_list = [pd.read_pickle(file) for file in file_list]
	df = pd.concat(df_list)
	return df

def	plot_ohlc(df):
	df.dropna()
	df = df.reset_index()
	df['RateDateTime'] = df['RateDateTime'].map(mdates.date2num)
	ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
	#ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
	ax1.xaxis_date()
	
	candlestick_ohlc(ax1, df.values, width=2, colorup='g')
	plt.show()


def main():
	download_data_and_resample('EUR_USD', datetime.date(2017,1,1), datetime.date(2017,6,25))
	df = create_dataframe("EUR_USD", "1D", datetime.date(2017,1,1), datetime.date(2017,6,25))
	#plot_ohlc(df['RateBid'])
	get_support_and_resistance(df, "1D")
	
if __name__ == '__main__':
		main()