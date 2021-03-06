'''
Created on 29 Apr 2017

@author: Gayan
'''
import urllib
import datetime
from datetime import timedelta, date
import calendar
import urllib
import re

download_site = 'http://ratedata.gaincapital.com/'
from requests import get
from io import BytesIO
from zipfile import ZipFile
 
def download_unzip(url, path):
	request = get(url)
	zip_file = ZipFile(BytesIO(request.content))
	#zip_file.extractall(
	files = zip_file.namelist()
	print(files)
	
def week_of_month(tgtdate):
	days_this_month = calendar.mdays[tgtdate.month]
	for i in range(1, days_this_month):
		d = datetime.date(tgtdate.year, tgtdate.month, i)
		if d.day - d.weekday() > 0:
			startdate = d
			break
	return (tgtdate - startdate).days //7 + 1
	
def date_range(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + timedelta(n)
	
def prepare_download_urls(pair, from_date, to_date):
	urls = []
	wmp = week_of_month(from_date)
	if wmp != 0:
		urls.append(download_site + from_date.strftime('%Y') + '/' + from_date.strftime('%m') + ' ' + from_date.strftime("%B") + '/' + pair + '_Week' + '{}'.format(wmp) + '.zip')
	for single_date in date_range(from_date, to_date):
		wm = week_of_month(single_date)
		if wm != wmp and wm != 0:
			wmp = wm
			urls.append(download_site + single_date.strftime('%Y') + '/' + single_date.strftime('%m') + ' ' + single_date.strftime("%B") + '/' + pair + '_Week' + '{}'.format(wmp) + '.zip')
	print (urls)
	return urls		

def download_historical_data(pair, from_date, to_date):
	urls = prepare_download_urls(pair, from_date, to_date)
	for url in urls:
		ids = url.split('/')
		print(ids)
		path = ids[3] + '_' + re.sub(r'\D', '',ids[4]) + '_' +  ids[5].translate(None, '.zip')
		download_unzip(url, path)
		
	