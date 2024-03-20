#!/usr/bin/env python3
'''
    Testing overriding parameters that are
    boolean in the yaml file eg process_entire_database

    The problem is that when provided as override it
    will turn into a <str> datatype.
'''

import sys
import qadoemdbetl
import validate
# import os
import yaml
import argparse
import socket
import logging
import time

hostname = socket.gethostname()
process_functions = []
list_of_bool = ['gc_compat',
                'drop_table_if_exists',
                'etl',
                'process_entire_database',
                'quit_on_table_error',
                'create_mdb',
                'mandatory_to_not_null',
                'stop_on_duplicate',
                'stop_on_error',
                'require_empty_table',
                'skip_table_with_data',
                'cassandra_ignore_highwater',
                'push_daemon_mode',]


def _get_config(cfgfile):
    '''
        Read the yaml configuration file
    '''
    try:
        with open(cfgfile, 'r') as f:
            cfg = yaml.safe_load(f)
        return cfg
    except FileNotFoundError:
        print('Cannot load YAML config file %s' % cfgfile)
    except yaml.YAMLError as e:
        print('Error parsing YAML config file %s - %s' % (cfgfile, e))
    sys.exit(2)


def add_arguments(parser, cfg):
    '''
        Add all configuration settings as (possible) argument to parser
    '''
    parser.add_argument('--cfg')
    for arg in cfg.keys():
        '''
        if 'pass' in arg:
            print('Adding Argument %s with HIDDEN value' % (arg))
        else:
            print('Adding Argument %s with default value: %s ' % (arg, cfg[arg]))
        '''
        parser.add_argument('--%s' % arg)
    return parser


def process_overrides(args, cfg):
    '''
        Override configuration setting when argument is supplied
    '''
    for key, value in vars(args).items():
        if key == 'cfg':
            continue
        if value is None:
            continue
        if key in list_of_bool:
            print('Overriding boolean setting for %s to %s' % (key, value))
            v = value.capitalize()
            if v in ('True', 'False'):
                cfg[key] = eval(v)
            else:
                print('Override of %s ignored - can only be True or False' %
                      key)
        else:
            print('Overriding %s setting to %s' % (key, value))
            cfg[key] = value
    return cfg


def elapsed_time(start_time):
    '''
        Print duration of process
    '''
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    return


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print('Usage :  oemdbetlharness.py --cfg cfgfile [--arg value --arg value]')
        print('Missing cfgfile.  Exiting')
        sys.exit(2)

    if not sys.argv[1] == '--cfg':
        print('%s not recognized' % (sys.argv[1]))
        print('Usage :  oemdbetlharness.py --cfg cfgfile [--arg value --arg value]')
        sys.exit(2)

    start_time = time.time()

    cfgfile = sys.argv[2]
    cfg = _get_config(cfgfile)

    parser = argparse.ArgumentParser()
    parser = add_arguments(parser, cfg)

    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(2)

    cfg = process_overrides(args, cfg)

    print('Value of etl: %s' % cfg['etl'])
    print('Type of etl: %s' % type(cfg['etl']))

    print('Checking some if-statements for etl:')
    if cfg['etl']:
        print('\tif with no operand')
    if cfg['etl'] == True:
        print('\tif with "==" operand')
    if cfg['etl'] is True:
        print('\tif with "is" operand')
    print('Checking some if-statements for process_entire_database:')
    if cfg['process_entire_database']:
        print('\tif with no operand')
    if cfg['process_entire_database'] == True:
        print('\tif with "==" operand')
    if cfg['process_entire_database'] is True:
        print('\tif with "is" operand')

'''
    conn = False

    print('*** Beginning ETL Process ***')
    print('We are going to Run the following functions:')
    pf = cfg['process_functions'].split(',')

    for line in pf:
        line = line.strip()
        # this is just to handle if someone put spaces in the YAML file
        process_functions.append(line)
        print(line)

        # If we are Loading, we need to connect to MariaDB
        if 'load' in line:
            conn = True

    if eval(cfg['process_entire_database']) is True:
        print('On the entire %s/%s database' % (cfg['oedbpath'], cfg['oedbname']))
    else:
        print('On the following tables in database %s/%s: %s' % (
            cfg['oedbpath'], cfg['oedbname'], cfg['include_tables']))
    print('The following tables are excluded : %s' % (cfg['exclude_tables']))

    print('Refer to %s for the etl logs, and %s for the etl error messages' % (
        cfg['logfile'], cfg['logerror']))

    # Setup logging
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    print(cfg['loglevel'])
    if cfg['loglevel'] == 'ERROR':
        error_handler = logging.FileHandler(cfg['logerror'])
        error_handler.setLevel(logging.ERROR)
        logger.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)
    else:
        logger.setLevel(logging.INFO)

        info_handler = logging.FileHandler(cfg['logfile'])
        info_handler.setFormatter(formatter)
        logger.addHandler(info_handler)

    if cfg['loglevel'] == 'DEBUG':
        logger.setLevel(logging.DEBUG)

    logger.debug('Debug message Example')
    logger.info('Info message Example')
    logger.warning('Warning message Example')
    logger.error('Error message Example')
    logger.critical('Critical message Example')

    if cfg['create_mdb']:
        # try to create database in MariaDb (if not exists)
        logger.info('Trying to create databases in MariaDb')
        # try MariaDB connect
        tmp_db = cfg['mdbname']
        cfg['mdbname'] = ''
        conn = qadoemdbetl.conn_mariadb(cfg, logger)
        if conn is False:
            print('Because we are trying to create the databases we cannot connect to MariaDB')
            print('The conversion process is prematurely exiting.')
            elapsed_time(start_time)
            sys.exit(2)

        dblist = tmp_db + ',' + cfg['mdbname_cust']
        for db in dblist.split(','):
            logger.info('Creating database %s' % db)
            qry = 'create database if not exists %s' % db
            result = qadoemdbetl.run_msql(qry, conn, cfg, logger)
            if result is False:
                print('Unable to create database %s' % db)
                sys.exit(2)

        cfg['mdbname'] = tmp_db

    if conn is True:
        # try MariaDB connect
        conn = qadoemdbetl.conn_mariadb(cfg, logger)
        if conn is False:
            print('Because we are Loading data and we cannot connect to MariaDB')
            print('The conversion process is prematurely exiting.')
            elapsed_time(start_time)
            sys.exit(2)

        print('Connected to MariaDB')

    # note, upon termination we do not need to explicitly disconnect from MariaDB

    # If we are processing the entire database, the functions should be run in this order
    # You can runtime or YAML file override , of course

    if 'extractSchema' in process_functions:
        result = qadoemdbetl.extract(cfg, logger, 'extractSchema')
        if result is False:
            print('Error in extractSchema, see error log, exiting now')
            elapsed_time(start_time)
            sys.exit(0)

    if 'extractIndex' in process_functions:
        result = qadoemdbetl.extract(cfg, logger, 'extractIndex')
        if result is False:
            print('Error in extractIndex, see error log, exiting now')
            elapsed_time(start_time)
            sys.exit(0)

    if 'extractData' in process_functions:
        result = qadoemdbetl.extract(cfg, logger, 'extractData')
        if result is False:
            print('Error in extractData, see error log, exiting now')
            elapsed_time(start_time)
            sys.exit(0)

    if 'extractSequence' in process_functions:
        result = qadoemdbetl.extractSequence(cfg, logger, 'extractSequence')
        if result is False:
            print('Error in extractSequence, see error log, exiting now')
            elapsed_time(start_time)
            sys.exit(0)

    if 'validateSchema' in process_functions:
        result = validate.validateSchema(cfg, logger, 'validateSchema')
        if result is False:
            print('Error in validateSchema, see error log, exiting now')
            elapsed_time(start_time)
            sys.exit(0)

    if 'validateIndex' in process_functions:
        result = validate.validateIndex(cfg, logger, 'validateIndex')
        if result is False:
            print('Error in validateIndex, see error log, exiting now')
            elapsed_time(start_time)
            sys.exit(0)

    if 'validateSequence' in process_functions:
        result = validate.validateSequence(cfg, logger, 'validateSequence')
        if result is False:
            print('Error in validateSequence, see error log, exiting now')
            elapsed_time(start_time)
            sys.exit(0)

    if 'loadSchema' in process_functions:
        result = qadoemdbetl.load(cfg, logger, 'loadSchema', conn)
        if result is False:
            print('Error in loadSchema, see error log, exiting now')
            elapsed_time(start_time)
            sys.exit(0)

    if 'loadIndex' in process_functions:
        result = qadoemdbetl.load(cfg, logger, 'loadIndex', conn)
        if result is False:
            print('Error in loadIndex, see error log, exiting now')
            elapsed_time(start_time)
            sys.exit(0)

    if 'loadData' in process_functions:
        result = qadoemdbetl.load(cfg, logger, 'loadData', conn)
        if result is False:
            print('Error in loadData, see error log, exiting now')
            elapsed_time(start_time)
            sys.exit(0)

    # we need to create the FWD sequence p2j_id_generator_sequence in addition to the QAD sequences
    if 'loadSequence' in process_functions:
        result = qadoemdbetl.loadSequence(cfg, logger, conn)
        if result is False:
            print('Error in loadSequence, see error log, exiting now')
            elapsed_time(start_time)
            sys.exit(0)

    print('Finished')
    elapsed_time(start_time)

    sys.exit(0)
'''
