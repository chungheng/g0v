#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join
from collections import defaultdict
import numpy as np
import csv
import json
import io

mypath = "../../data/"
files = [ f for f in listdir(mypath) \
		if isfile(join(mypath,f)) and u'立法委員'.encode('utf-8') in f and u'專戶.csv'.encode('utf-8') in f]
expense_type = (
	u'雜支支出'.encode('utf-8'),
	u'公共關係費用支出'.encode('utf-8'),
	u'利用宣傳車輛支出'.encode('utf-8'),
	u'返還支出'.encode('utf-8'),
	u'交通旅運支出'.encode('utf-8'),
	u'租用競選辦事處支出'.encode('utf-8'),
	u'租用競選辦事處支'.encode('utf-8'),
	u'租用競選辦事處'.encode('utf-8'),
	u'宣傳支出'.encode('utf-8'),
	u'集會支出'.encode('utf-8'),
	u'人事費用支出'.encode('utf-8'),
	u'繳庫支出'.encode('utf-8'),
	u'租用宣傳車輛支出'.encode('utf-8'),
	u'交通旅費支出'.encode('utf-8'))
expense_idx = 5

income_type = (
	u'營利事業捐贈收入'.encode('utf-8'),
	u'人民團體捐贈收入'.encode('utf-8'),
	u'匿名捐贈'.encode('utf-8'),
	u'政黨捐贈收入'.encode('utf-8'),
	u'個人捐贈收入'.encode('utf-8'),
	u'其他收入'.encode('utf-8'))
income_idx = 4

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

def csv_to_json():
	for f in files:
		with io.open(join(mypath,f), 'r', encoding='utf8') as csvfile:
			jsonfilename = (mypath+f).replace('csv','json')
			jsonfile = open(jsonfilename, 'w')
			reader = csv.DictReader( csvfile )
			for row in reader:
				data = json.dumps( row, ensure_ascii=False, encode='utf8')
				jsonfile.write(data)
				jsonfile.write('\n')
		break

def cong_cat():
	cong_dict = {find_between( f, u'參選人'.encode('utf-8'),u'政治'.encode('utf-8')):np.zeros(2,dtype=int) for f in files}
	com_dict = {}
	for f in files:
		print "parse: %s" % f

		in_dict = {f:defaultdict(int) for f in income_type}
		exp_dict = {f:defaultdict(int) for f in expense_type}
		with open(join(mypath,f), 'rb') as csvfile:
			csv_row = csv.reader(csvfile, delimiter=',')
			next(csv_row)
			for row in csv_row:
				inexp_type = row[1].strip(' ')
				if row[income_idx] != "":
					if inexp_type not in income_type:
						continue
					name = row[2].strip(' ')
					in_dict[inexp_type][name] += int(row[income_idx])
				elif row[expense_idx] == "":
					continue
				else:
					if inexp_type not in expense_type:
						continue
					name = row[2].strip(' ')
					exp_dict[inexp_type][name] += int(row[expense_idx])
			exp_dict[u'交通旅費支出'.encode('utf-8')].update(exp_dict[u'交通旅運支出'.encode('utf-8')])
			exp_dict[u'租用競選辦事處支出'.encode('utf-8')].update(exp_dict[u'租用競選辦事處'.encode('utf-8')])
			exp_dict[u'租用競選辦事處支出'.encode('utf-8')].update(exp_dict[u'租用競選辦事處支'.encode('utf-8')])
			del exp_dict[u'交通旅運支出'.encode('utf-8')]
			del exp_dict[u'租用競選辦事處支'.encode('utf-8')]
			del exp_dict[u'租用競選辦事處支出'.encode('utf-8')]

		with open(join("Income_"+f), 'w') as csvfile:
			for t, d in in_dict.items():
				for c,m in d.items():
					csvfile.write("%s-%s,%d\n" % (t,c,m))

if __name__ ==  "__main__":
	# csv_to_json()
	# get_company("公司支出收入.csv")
	cong_cat()
