#!/usr/bin/env python3
'''
	Use mylib.py
'''

import logging
import sys
from rich import print
from rich.logging import RichHandler
from mylib import p1,p2
#import mylib


def myopen(file):
	'''
		Use p1 from mylib to read file
	'''
	logging.info('Running myopen with %s' % file)
	lines = p1(file)
	return lines

if __name__ == "__main__":

	# Set up logging
	#formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	formatter = '%(message)s'
	logging.basicConfig(
		#level=logging.INFO, format=formatter, datefmt="[%X]", handlers=[logging.StreamHandler()]
		level=logging.INFO, format=formatter, datefmt="[%X]", handlers=[RichHandler()]
	)
	
	if p2:
		logging.info('p2 is True')
		a = p1('pipo')
		if not a == False:
			print(a)

	logging.info('Calling myopen')
	a = myopen('pipo')
	if not a == False:
		print(a)
	else:
		logging.warning('myopen failed')

	try:
		b = myopen('mylib.py')
	except Exception as e:
		pass

	if not b == False:
		data = []
		for line in b:
			line = line.strip()
			data.append(line)
		print(data)
