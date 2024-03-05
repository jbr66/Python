#!/usr/bin/python3
'''
NAME
	simpleLog.py	-	Setup logging with config file

'''

import logging
import logging.config

logging.config.fileConfig('logging.conf')

# Create logger
logger = logging.getLogger('simpleExample')

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critical message')
