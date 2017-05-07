'''
Created on 29 Apr 2017

@author: Gayan
'''
import urllib
from datetime import datetime
from datetime import timedelta, date
import pandas as pd


download_site = 'http://ratedata.gaincapital.com'
	
def date_range(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + timedelta(n)
	
def prepare_download_urls(from_date, to_date):
	for single_date in date_range(from_date, to_date):
		print(single_date.strftime("%Y-%m-%d"))

def download_historical_data(pair, from_date, to_date):
	url = prepare_download_urls(from_date, to_date)
	
def gain_parser(dt_str):
	try:
		return datetime.strptime(dt_str[:-3],'%Y-%m-%d %H:%M:%S.%f')
	except Exception as e:
		return datetime.strptime(dt_str,'%Y-%m-%d %H:%M:%S')
	
def parse_csv(filename):
	df = pd.read_csv(filename, parse_dates=['DateTime'], index_col='DateTime', names=['Tid', 'Dealable', 'Pair', 'DateTime', 'Buy', 'Sell'], date_parser=gain_parser)
	del df['Tid'] 
	del df['Dealable']
	del df['Pair']
	grouped_data = df.resample('15Min', how='ohlc')
	grouped_data.to_pickle(filename+'-OHLC.pkl')
