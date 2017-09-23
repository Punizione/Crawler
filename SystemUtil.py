# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

def pause(delay, stuNumber):
	print('Now is %s\'s PauseTime'%stuNumber)
	time.sleep(delay)
	print('%s\'s PauseTime Over'%stuNumber)
