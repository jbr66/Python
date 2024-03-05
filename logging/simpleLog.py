#!/usr/bin/python3
'''
NAME
	simpleLog.py	-	Setup logging with config file

'''

import logging
import logging.config
import yaml
import sys

file = 'logging.yaml'

try:
	with open(file,'r') as f:
		logconfig = yaml.safe_load(f)
except Exception as e:
	print('Error reading %s - %s' % (file,e))
	sys.exit(1)

#logging.config.fileConfig('logging.conf')
logging.config.dictConfig(logconfig)

# Create logger
logger = logging.getLogger('simpleExample')

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critical message')
