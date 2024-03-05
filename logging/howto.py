#!/usr/bin/python3
'''
NAME
	howto.py	-	How to use logging

	10 DEBUG
	20 INFO
	30 WARNING
	40 ERROR
	50 CRITICAL

DESCRIPTION
	In this example the console will display WARNING or higher, but in the 
	logfile everything will be logged. What will be logged depends on 
	logger.getEffectiveLevel()

USAGE
	usage: howto.py [-h] [-e ERRORLEVEL] [-f ERRORLOG]
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -e ERRORLEVEL, --errorLevel ERRORLEVEL
	                        Set errorlevel for console output
	  -f ERRORLOG, --errorLog ERRORLOG
	                        Set logfile for logging output
'''

import logging
import time
import argparse
import sys
from mylog import printLog

validLevels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--errorLevel', dest='errorLevel', type=str,
	default='WARNING', help='Set errorlevel for console output')
parser.add_argument('-f', '--errorLog', dest='errorLog', default='howto.log',
	help='Set logfile for logging output')

args = parser.parse_args()

logFile = args.errorLog
errorLevel = args.errorLevel.upper()

if not errorLevel in validLevels:
	print('%s is not a valid error level' % errorLevel)
	print('Valid levels are %s' % ', '.join(i for i in validLevels))
	sys.exit(99)

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
	ch.setLevel(errorLevel) 	# by default WARNING or higher will be displayed
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
