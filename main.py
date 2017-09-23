# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import FileUtil
import SystemUtil
import ConnectUtil
from ThreadForLogin import MyThread

def work(count):
	"""
	count:Count of Thread
	"""
	Threads = []
	stuNumberArray = FileUtil.div_list(FileUtil.getStuNumber(),count)
	for i in range(0,count):
		Threads.append(MyThread('Thread%d'%i, i, stuNumberArray[i], FileUtil.getRandom()))

	for t in Threads:
		t.start()

	for t in Threads:
		t.join()

	print('All Thread Has Refused')


if __name__ == '__main__':
	work(1)