# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import http.cookiejar
import random
import urllib.request
import urllib.parse

import Constant
import FileUtil
import re
from urllib.error import URLError,HTTPError
import math

userAgents = ['Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);',
			  'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
			  'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)',
			  'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11',
			  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2',
			  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
			  'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
			  'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
			  'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25']


def getUrlOpener():
	global userAgents


	cj = http.cookiejar.CookieJar()

	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPHandler)
	opener.addheaders = [('User-agent', random.choice(userAgents)),
						 ('Host', 'jwxt.gduf.edu.cn'),
						 ('Origin', 'http://jwxt.gduf.edu.cn'),
						 ('Content-Type','application/x-www-form-urlencoded')]

	opener = autoLoginFirst(opener)
	return opener


def autoLoginFirst(opener):
	username = Constant.username
	password = Constant.password

	postUrl = 'http://jwxt.gduf.edu.cn/jsxsd/xk/LoginToXK'
	postData = urllib.parse.urlencode({'encoded':encodeInp(username)+'%%%'+encodeInp(password)}).encode('utf-8')
	try:
		opener.open(postUrl, postData)
	except:
		print('Auto Login Fail')
		return None
	return opener


def doPost(opener, stuNumber, salt):
	if not opener:
		raise HTTPError
	postUrl = 'http://jwxt.gduf.edu.cn/Logon.do?method=logonFromJsxsd/'
	postData = {'view':'',
				'useraccount':stuNumber,
				'ticket':stuNumber+'#'+salt}
	postData = urllib.parse.urlencode(postData).encode('utf-8')

	try:
		f = opener.open(postUrl, postData)
		response = f.read().decode('utf-8')

		userId = FileUtil.getUserId(response)
		userPwd = FileUtil.getPassWord(response)

		if not (userId.strip()=='' and userPwd.strip()==''):
			success = True
			data = {'success':True,
					'data':{
						'userid':userId,
						'password':userPwd
					}}
		else:
			data = {'success':False}

		return data
	except:
		print('Getting %s Fail'%stuNumber)
		return {'success':False}





def encodeInp(input):
	keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
	output = ""
	chr1, chr2, chr3 = "","",""
	enc1, enc2, enc3, enc4 = "","","",""
	i = 0
	while True:
		if i<len(input):
			chr1 = ord(input[i])
			i+=1
		if i<len(input):
			chr2 = ord(input[i])
			i+=1
		if i<len(input):   
			chr3 = ord(input[i])
			i+=1

		enc1 = chr1 >> 2
		
		if not chr2=='':
			enc2 = ((chr1 & 3) << 4) | (chr2 >> 4)
		else:
			enc2 = ((chr1 & 3) << 4)

		if not chr2=='':
			if not chr3=='':
				enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
				enc4 = chr3 & 63
			else:
				enc3 = ((chr2 & 15) << 2)
				
		if not chr2=='':
			if math.isnan(chr2):
				enc3 = enc4 = 64
		else:
			enc3 = enc4 = 64
		if not chr3=='':
			if math.isnan(chr3):
				enc4 = 64
		else:
			enc4 = 64
		output = output + chr(ord(keyStr[enc1])) + chr(ord(keyStr[enc2])) + chr(ord(keyStr[enc3])) + chr(ord(keyStr[enc4]))
		chr1 = chr2 = chr3 = ""
		enc1 = enc2 = enc3 = enc4 = ""
		if i >= len(input):
			break
	return output
