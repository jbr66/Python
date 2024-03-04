#!/usr/bin/python3
'''
NAME
	howto.py	-	How to use logging
'''

import logging

def printLog(logger, level):
	logger.debug('This is a debug message - %d' % level)
	logger.info('This is a info message - %d' % level)
	logger.warning('This is a warning message - %d' % level)
	logger.error('This is a error message - %d' % level)
	logger.critical('This is a critical message - %d' % level)

if __name__ == '__main__':
# Setup logging
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.WARNING)

	# Logfile log output
	error_handler = logging.FileHandler('howto.log')
	error_handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	error_handler.setFormatter(formatter)

	# Console log output
	ch = logging.StreamHandler()
	ch.setLevel(logging.ERROR)
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
	ch.setFormatter(formatter)
	
	logger.addHandler(error_handler)
	logger.addHandler(ch)

	level = logger.getEffectiveLevel()
	printLog(logger,level)

	print('Changing level to INFO')
	logger.setLevel('INFO')
	level = logger.getEffectiveLevel()
	printLog(logger,level)
	
