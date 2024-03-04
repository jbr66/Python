#!/usr/bin/python3
'''
NAME
	howto.py	-	How to use logging

	10 DEBUG
	20 INFO
	30 WARNING
	40 ERROR
	50 CRITICAL

In this example the console will display WARNING or higher, but in the logfile
everything will be logged. What will be logged depends on logger.getEffectiveLevel()
'''

import logging
import time

def printLog(logger, level):
	logger.debug('This is a debug message - %d' % level)
	logger.info('This is a info message - %d' % level)
	logger.warning('This is a warning message - %d' % level)
	logger.error('This is a error message - %d' % level)
	logger.critical('This is a critical message - %d' % level)

logFile = 'howto.log'
if __name__ == '__main__':
	# Setup logging
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)

	# Logfile log output
	fh = logging.FileHandler(logFile)
	fh.setLevel(logging.DEBUG)	# Everything will be logged - based on logger.setLevel
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)

	# Console log output
	ch = logging.StreamHandler()
	ch.setLevel(logging.WARNING) 	# WARNING or higher will be displayed
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
	ch.setFormatter(formatter)
	
	logger.addHandler(fh)
	logger.addHandler(ch)

	level = logger.getEffectiveLevel()
	print('Initial setting for logging: %d' % level)
	printLog(logger,level)

	# Pause for 3 seconds
	time.sleep(3)

	print('Changing level to DEBUG')
	logger.setLevel(logging.DEBUG)
	level = logger.getEffectiveLevel()
	printLog(logger,level)
	
	# Pause for 3 seconds
	time.sleep(3)

	print('Changing level to ERROR')
	logger.setLevel('ERROR')
	level = logger.getEffectiveLevel()
	printLog(logger,level)
