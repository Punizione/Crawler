# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
import sys
import random
import codecs
import math

def saveInfo(data, threadNumber):
	if not os.path.exists('e:/UserFromSystem'):
		os.mkdir(r'e:/UserFromSystem')

	f = open('e:\\UserFromSystem\\PassWordInfo'+threadNumber+'.txt','a+')

	if data['userid'].strip()=='' :
		f.close()
		print('Data Error')
		return False
	else:
		f.write(data['userid'])
		f.write('\t')
		f.write(data['password'])
		f.write('\n')
		f.close()
		print('Thread-%s Get and Save PassWord Success'%threadNumber)
		return True

def getPassWord(data):
	pattern = re.compile(r"var userpsw = '(.+?)';",re.S)
	userpwd = re.findall(pattern, data)
	if len(userpwd) == 0:
		return ''
	if userpwd:
		return userpwd[0]
	else:
		return ''


def getUserId(data):
	pattern = re.compile(r"var userid = '(.+?)';",re.S)
	userid = re.findall(pattern, data)

	if len(userid) == 0:
		return ''
	if userid:
		return userid[0]
	else:
		return ''

def getStuNumber(path=None):
	if not path:
		path = 'e:\\UserFromSystem\\UserInfo.txt'
	with codecs.open(path, encoding='utf-8') as f:
	#f = open(path,'r')
		lines = f.readlines()
		stuNumberArray = []
		for line in lines:
			stuNumber = line[0:9]
			stuNumberArray.append(stuNumber)

		print('Get StuNumber From LocalSystem Success')
		f.close()
	return stuNumberArray

def div_list(ls,n):
	"""

	"""
	if not isinstance(ls,list) or not isinstance(n,int):
		return []

	ls_len = len(ls)
	if n<=0 or ls_len==0:
		return []
	if n>ls_len:
		return []
	elif n == ls_len:
		return [[i] for i in ls]
	else:
		j = (int)(ls_len/n)
		k = ls_len%n
		ls_return = []
		for i in range(0,(n-1)*j,j):
			ls_return.append(ls[i:i+j])
		ls_return.append(ls[(n-1)*j:])
		return ls_return

def getRandom():
	return str(random.randrange(10000000,99999999))