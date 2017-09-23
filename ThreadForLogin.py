# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import threading

import time

import ConnectUtil
import FileUtil
import SystemUtil
class MyThread(threading.Thread):
	def __init__(self, number, delay, stuNumber, salt):
		super(MyThread, self).__init__()
		self.delay = delay
		self.number = number
		self.stuNumber = stuNumber
		self.salt = salt


	def run(self):
		print('This is Thread-%s' %self.number)
		time.sleep(self.delay)
		for i in self.stuNumber:
			print('Start %s ...' % i)
			opener = ConnectUtil.getUrlOpener()
			try:
				response = ConnectUtil.doPost(opener, self.stuNumber, self.salt)
				if response['success']:
					FileUtil.saveInfo(response['data'], self.number)
				else:
					print('Connet Success But Getting %s Fail'% i)
					#FileUtil.saveError(i)
			except:
				print('Connect Error, Getting %s Fail' % i)
				#FileUtil.saveErroe(i)
			SystemUtil.pause(self.delay, i)



