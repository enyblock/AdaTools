#!/usr/bin/python
#coding=utf-8

#https://api.binance.com/api/v1/trades?symbol=ADABTC
#https://api.binance.com/api/v1/trades?symbol=ADAETH
#https://otcbtc.com/sell_offers?currency=btc&fiat_currency=cny&payment_type=all
#https://otcbtc.com/sell_offers?currency=eth&fiat_currency=cny&payment_type=all
#10000 ==> 1819.23 

import re
import time
import requests
import simplejson
from bs4 import BeautifulSoup

URL_BINANCE = 'https://api.binance.com/api/v1/trades'
URL_OTCBTC_START  = 'https://otcbtc.com/sell_offers?currency='
URL_OTCBTC_END    = '&fiat_currency=cny&payment_type=all'

def get_binance(type):
	r = requests.get(URL_BINANCE, params = {'symbol':'ADA'+type.upper()})
	ret_dict = simplejson.loads(r.text.encode('gbk'))
	return float(ret_dict[0]['price'])

def get_otcbtc(type):
	response = requests.get(URL_OTCBTC_START+type+URL_OTCBTC_END)
	soup = BeautifulSoup(response.text.encode("utf8"), "html.parser")
	t_num_str = "".join(soup.find_all("div", class_="recommend-card__price")[0].text.encode('gbk').split()).replace(',','')
	return float(t_num_str)

def calculate_ada_num(orig, bin_p, otcbtc_p):
	ada_num = orig/otcbtc_p-0.001
	ada_num /= bin_p
	ada_num *= 0.999
	return (ada_num-1)

def show_msg(orig, type):

	t_bin_p    = get_binance(type) 
	t_otcbtc_p = get_otcbtc(type)
	t_ada_num  = calculate_ada_num(orig, t_bin_p, t_otcbtc_p)

	print '{} CNY {:.2f} ==> {:^8d} {} ==> {:.8f} ADA : {}'.format(orig, orig/t_ada_num, int(t_otcbtc_p), type.upper(), t_bin_p, t_ada_num)
	

def loop_show():
	while True:
		show_msg(10000, 'eth')
		show_msg(10000, 'btc')
loop_show()

# print(get_binance('eth'))
# print(get_otcbtc('eth'))