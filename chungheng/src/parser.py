#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join
import numpy as np
import csv

mypath = "../data/"
files = [ f for f in listdir(mypath) \
		if isfile(join(mypath,f)) and u'立法委員'.encode('utf-8') in f]

def find_between( s, first, last ):
	try:
		start = s.index( first ) + len( first )
		end = s.index( last, start )
		return s[start:end]
	except ValueError:
		return ""

def get_company(filename):
	cong_dict = {find_between( f, u'參選人'.encode('utf-8'),u'政治'.encode('utf-8')):np.zeros(2,dtype=int) for f in files}
	com_dict = {}
	for f in files:
		cong_name = find_between( f, u'參選人'.encode('utf-8'),u'政治'.encode('utf-8'))
		with open(join(mypath,f), 'rb') as csvfile:
			csv_row = csv.reader(csvfile, delimiter=',')
			next(csv_row)
			for row in csv_row:
				com_name = row[2]
				if com_name not in com_dict:
					com_dict[com_name] = cong_dict.copy()
				if row[4]:
					com_dict[com_name][cong_name][0] += int(row[4])
				if row[5]:
					com_dict[com_name][cong_name][1] += int(row[5])
	fout = open(filename, 'w')
	fout.write("公司名稱")
	for name in cong_dict.keys():
		fout.write(",%s,收入,支出" % name)
	fout.write("\n")
	for com, data in com_dict.items():
		fout.write(com)
		for name, m in data.items():
			fout.write(",%s,%d,%d" % (name, m[0], m[1]))
		fout.write("\n")



if __name__ ==  "__main__":

	get_company("公司支出收入.csv")
