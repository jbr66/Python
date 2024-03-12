#!/usr/bin/env python3
'''
	Some procedures to see how logging is handled
'''

import logging
import sys

def p1(file):
	logging.info('Procedure p1')
	try:
		with open(file,'r') as f:
			lines = f.readlines()
		return lines
	except Exception as e:
		logging.error('Failed to read file - %s' % e)

	return False

def p2(name):
	logging.info('Procedure p2 called with %s' % name)
	return True

if __name__ == "__main__":
	
	# Set up logging
	formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	logging.basicConfig(
		level=logging.INFO, format=formatter, datefmt="[%X]", handlers=[logging.StreamHandler()]
	)

	if p2:
		logging.info('p2 returned True')
		a = p1('x.py')
		print(a)
	

