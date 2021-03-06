
from __future__ import print_function

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import Formatter
from talib.abstract import *
from matplotlib.dates import AutoDateFormatter, AutoDateLocator, date2num, num2date
from ta_predict import *
from utility import *
import talib
import argparse
from collections import OrderedDict
import datetime
import math
import info_main
from kline import *

def main():
	if False:
		#update_daily_eps(2018, 1, 31)
		#print(get_daily_eps(2018, 1, 31))
		#empty, df_main = readStockHistory('3014', 9999)
		#stockList = readStockList('all_stock.csv')
		#for stock in stockList:
		#	print(stock)
		#df = financial_statement(2018, 1, '綜合損益彙總表')
		#print(df)
		#df = financial_statement(2018, 1, '資產負債彙總表')
		#print(df)
		#df = financial_statement(2018, 1, '營益分析彙總表')
		#print(df)
		pd.options.display.float_format = '{:.2f}'.format
		df_ROE=readROEHistory('ROE_2006_2017.csv', avg_min=0, std_max=70)
		df_ROE=df_ROE.drop(columns=[u'成交', u'漲跌價', u'漲跌幅', u'18Q1ROE(%)'])
		df_ROE['std_ROE']=df_ROE.std(axis=1, ddof=0)
		#print(df_ROE)
		
		df_ROE=df_ROE.sort_values(by=['avg_ROE'], ascending=False)
		df_ROE=df_ROE[df_ROE['avg_ROE']>0]
		df_ROE=df_ROE[df_ROE['std_ROE']<100]
		df_ROE.reset_index(inplace=True)
		df_ROE=df_ROE[['stock', 'name', 'ranking', 'avg_ROE', 'std_ROE', \
						'2017ROE', '2016ROE', '2015ROE', '2014ROE', '2013ROE', \
						'2012ROE', '2011ROE', '2010ROE', '2009ROE', '2008ROE', \
						'2007ROE', '2006ROE']]
		df_ROE['stock']=df_ROE['stock'].str.replace('=', '')
		df_ROE['stock']=df_ROE['stock'].str.replace('"', '')
		df_ROE.to_csv('test_result/ROE.csv', encoding='utf_8', float_format='%.2f')
		writer = pd.ExcelWriter('test_result/ROE.xlsx')
		df_ROE.to_excel(writer, float_format='%.2f')
		writer.save()
		
	if False:
		stockList = readStockList('all_stock.csv')
		for stock in stockList:
			df_main = pd.read_csv('history/'+stock+'.csv', delim_whitespace=False, header=0)
			if df_main.empty == True:
				print('no data')
				continue
			#if '2018-06-01' in df_main['DateStr'].values:
			dateStr = ['2018-05-31', '2018-06-01', '2018-06-04', '2018-06-05', '2018-06-06', '2018-06-07', '2018-06-08']
			for _date in dateStr:
				if _date not in df_main['DateStr'].values:
					continue
				vol = df_main['volume'].loc[df_main['DateStr']==_date].values[0]
				vol = float(int(vol/1000))
				df_main['volume'].loc[df_main['DateStr']==_date]=vol
			#df_main['volume'].loc[df_main['DateStr']=='2018-06-01']=df_main['volume'].loc[df_main['DateStr']=='2018-06-01']/1000
			#df_main['volume'].loc[df_main['DateStr']=='2018-06-04']=df_main['volume'].loc[df_main['DateStr']=='2018-06-04']/1000
			#df_main['volume'].loc[df_main['DateStr']=='2018-06-05']=df_main['volume'].loc[df_main['DateStr']=='2018-06-05']/1000
			#df_main['volume'].loc[df_main['DateStr']=='2018-06-06']=df_main['volume'].loc[df_main['DateStr']=='2018-06-06']/1000
			#df_main['volume'].loc[df_main['DateStr']=='2018-06-07']=df_main['volume'].loc[df_main['DateStr']=='2018-06-07']/1000
			#df_main['volume'].loc[df_main['DateStr']=='2018-06-08']=df_main['volume'].loc[df_main['DateStr']=='2018-06-08']/1000
			#print(df_main)
			df_main.to_csv('history.new/'+stock+'.csv')
	if False:
		df = pd.read_csv('history/8299.TWO.csv', delim_whitespace=False, header=0)
		df = df.dropna()
		df = df.drop('Adj Close', 1)
		df['Date'] = pd.to_datetime(df.Date)
		df['DateStr'] = df['Date'].dt.strftime('%Y-%m-%d')
		df.rename(columns={'Open': 'open', 'Close': 'close', \
						'High': 'high', 'Low': 'low', 'Volume': 'volume'
						}, inplace=True)
		df.reset_index(drop=True, inplace=True)
		print('')
		df.to_csv('history/8299.csv')

	if False:
		df = pd.read_csv('history/8299.csv', delim_whitespace=False, header=0, index_col=0)
		df['volume'] = df['volume']/1000
		df.to_csv('history/8299.csv')

	if False:
		stockList = readStockList('all_stock.csv')
		for stock in stockList:
			df_main = pd.read_csv('history/'+stock+'.csv', delim_whitespace=False, header=0, index_col=0)
			df_main.drop(columns=['Unnamed: 0.1', 'Unnamed: 0.1.1'], inplace=True)
			df_main.to_csv('history/'+stock+'.csv')

	if False:
		startDate = date(2018, 6, 2)
		update_daily_3j_period(startDate, '4M')
		
	if False:
		startDate = date(2016, 1, 4)
		update_daily_MI_QFIIS_period(startDate, '1d')
		
	if False:
		startDate = date(2018, 1, 4)
		foreign_buy, foreign_sell, trust_buy, trust_sell, dealer_buy, dealer_sell = \
					get_daily_3j('2330', 2018, 1, 4)
		print('{}, {}, {}, {}, {}, {}'.format(foreign_buy, foreign_sell, trust_buy, trust_sell, dealer_buy, dealer_sell))

	if False:
		startDate = date(2016, 1, 1)
		update_daily_3j_period(startDate, '1Y')
	
	if False:
		plt.rcParams['font.sans-serif'] = ['simhei']
		plt.rcParams['figure.figsize'] = [16, 9]	
		info_main.draw_share_holders('9921', u'股權分散表', 'share_holders.png')
	
	if False:
		#stockList = readStockList('policy/top_watch.csv')
		stockList = readStockList('policy/test1.csv')
		for stock in stockList:
			empty, df_price = readStockHistory(stock, 240, raw=False)
			_k = kline(stock, df_price)
			_k.pattern_recogintion()
			print('')
			#print(stock, '::', _val)
			pngName = 'test_result'+'/kline_test.png'
			draw = ta_draw(stock+'  '+'巨大 kline', df_price, None, pngName, pngSize=3, kLineWidth=1, kRectWidth=0.8)
			draw.draw_price_volume()
	if True:
		stockList = readStockList('policy/test1.csv')
		for stock in stockList:
			empty, df_price = readStockHistory(stock, 9999, raw=False)
			if empty == True:
				print('empty...')
				continue
			for index, row in df_price.iterrows():
				if row['kline'] == '':
					continue
				#if patterncolor[row['kline']]=='green' or patterncolor[row['kline']]=='red':
				print(row['DateStr'], patterncolor[row['kline']], row['kline'])
		
main()