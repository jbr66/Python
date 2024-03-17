def printLog(logger, level):
    logger.debug('This is a debug message - %d' % level)
    logger.info('This is a info message - %d' % level)
    logger.warning('This is a warning message - %d' % level)
    logger.error('This is a error message - %d' % level)
    logger.critical('This is a critical message - %d' % level)
