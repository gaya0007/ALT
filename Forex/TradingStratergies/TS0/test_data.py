# import modules
import pandas as pd
from datetime import datetime
import os 
import pickle
# define a parser, for the more recent timestamp
sample_periods = ['15Min', '1H', '4H', '1D']
def gain_parser(dt_str):
	try:
		return datetime.strptime(dt_str[:-3],'%Y-%m-%d %H:%M:%S.%f')
	except Exception as e:
		return datetime.strptime(dt_str,'%Y-%m-%d %H:%M:%S')
		
def read_resample_save(dir):
	for file in os.listdir(dir):
		if file.endswith('csv'):
			filename = dir + file
			eu = pd.read_csv(filename,index_col=3,date_parser=gain_parser)
			del eu['lTid'] 
			del eu['cDealable']
			del eu['CurrencyPair']
			grouped_data = eu.dropna()
			for per in sample_periods:
				grouped_data = eu.resample(per).ohlc()
				grouped_data.to_pickle(filename +'-' + per + '_OHLC.pkl')		
			os.remove(filename)
		
def get_csv_files_and_resample():
	for dir_name in os.listdir('./Data'):
		if os.path.isdir(os.path.join('./Data/', dir_name)):
			dir_name = './Data/'+ dir_name + '/'
			read_resample_save(dir_name)
		
def get_pkl_files(dir):
	file_list = []
	for file in os.listdir(dir):
		if file.endswith('.pkl'):
			file_list.append(file)
	return 	file_list
	
def read_sampled_files():
	for dir_name in os.listdir('./Data'):
		if os.path.isdir(os.path.join('./Data/', dir_name)):
			dir_name = './Data/'+ dir_name + '/'
			pkl_files = get_pkl_files(dir_name)
			for file in pkl_files:
				with open(dir_name + file, 'rb') as f:
					data = pickle.load(f)
				print "from file {}{}".format(dir_name,file)	
				print data['RateBid'].head()
				print data['RateBid'].tail()
				

#get_csv_files_and_resample()		
#read_sampled_files()