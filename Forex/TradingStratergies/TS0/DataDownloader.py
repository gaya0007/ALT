'''
Created on 29 Apr 2017

@author: Gayan
'''
import urllib
from datetime import datetime
from datetime import timedelta, date
import pandas as pd


class TickDownloader:
	'''
	classdocs
	'''
	download_site = 'http://ratedata.gaincapital.com'
	global gain_parser
	def __init__(self):
		'''
		Constructor
		'''
		
	def date_range(self, start_date, end_date):
		for n in range(int ((end_date - start_date).days)):
			yield start_date + timedelta(n)
	
	def prepare_download_urls(self, from_date, to_date):
		start_year = from_date.strftime("%Y")
		start_month = from_date.strftime("%B")
		start_week = from_date.strftime("%d")
		end_month = to_date.strftime("%B")
		end_week = to_date.strftime("%d")
		print('start year :{} start month:{} start_week:{} end_month:{} endweek:{}'.format(
			start_year, start_month, start_week, end_month, end_week))
		for single_date in self.date_range(from_date, to_date):
			print(single_date.strftime("%Y-%m-%d"))
		
		'''print('preparering download link for historicaldata {}'.format(timeframe))
		return '{}/'.format(self.download_site)'''
		
	def download_historical_data(self, pair, from_date, to_date):
		'''
		input pair : 'EUR_USD'
		input from_date : datetime.date(2017,1,1)
		input to_date : datetime.date(2017,1,1)  
		'''
		url = self.prepare_download_urls(from_date, to_date)
		'''ret = urllib.urlretrieve(url, '/HData/')
	print(ret)'''
	def gain_parser(dt_str):
		try:
			return datetime.strptime(dt_str[:-3],'%Y-%m-%d %H:%M:%S.%f')
		except Exception as e:
			return datetime.strptime(dt_str,'%Y-%m-%d %H:%M:%S')
	
	def parse_csv(self, filename):
		df = pd.read_csv(filename, parse_dates=['DateTime'], index_col='DateTime', names=['Tid', 'Dealable', 'Pair', 'DateTime', 'Buy', 'Sell'], date_parser=gain_parser)
		del df['Tid'] 
		del df['Dealable']
		del df['Pair']
		grouped_data = df.resample('15Min', how='ohlc')
		grouped_data.to_pickle(filename+'-OHLC.pkl')
