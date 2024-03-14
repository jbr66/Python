#!/usr/bin/python3
'''
NAME
    getschema.py    -   Get the schema of a given database

Using config.yaml file:

	user: root
	password: xxxx
	host: 192.168.1.40
	port: 3306
	database: nation
'''

import mariadb
import yaml
import json
import argparse
import os, sys
import glob
import logging

'''
    Questions:
        blob -> mediumtext (longblob)
        datetime-tz -> datetime + offset field (timestamp/int)
        raw -> mediumtext (varbinary)
'''

map_dt_oem_mdb = [
        ('character', 'varchar'),
        ('character', 'text'),
        ('clob', 'mediumtext'),
        ('logical', 'tinyint'),
        ('integer', 'int'),
        ('int64', 'bigint'),
        ('date', 'date'),
        ('datetime', 'datetime'),
        ('decimal', 'decimal'),
        ('blob', 'longblob'),
        ('datetime-tz', 'timestamp'),
        ('datetime-tz', 'int'),
        ('raw', 'varbinary'),
        ]

'''
    DataType in MariaDB without format
'''

dt_no_fmt = [
        'text',
        'date',
        'mediumtext',
        'longblob',
        'timestamp',
        ]

valid_loglevel = [
        'DEBUG',
        'INFO',
        'WARNING',
        'ERROR',
        'CRITICAL',
        ]

def con_mariadb(cfg, mdb):
    '''
    Connect to MariaDb mdb from configfile, will return the connection
    '''
    try:
        conn = mariadb.connect(
            user     = cfg['user'],
            password = cfg['password'],
            host     = cfg['host'],
            port     = cfg['port'],
            database = mdb
        )
        return conn
    except mariadb.Error as e:
        print('Error connecting to MariaDB Platform %s' % e)
        sys.exit(1)

def mdb_gettables(conn):
    '''
    Returns dictionary of tables
    '''

    tables = {}
    # Get cursor
    _cur  = conn.cursor()

    _cur.execute('SHOW tables')

    for t in _cur:
        tables[t[0]] = {}

    return tables

def mdb_getfields(conn, table):
    '''
    Returns dictionary of fields for given table
    '''

    fields = {}
    # Get cursor
    _cur = conn.cursor()

    qry = 'describe %s' % table
    _cur.execute(qry)
    for f, t, n, k, d, e in _cur:
        fields[f] = {}
        if '(' in t:
            type = t.strip().split('(')[0]
            format = t.strip().split('(')[1][:-1]
        else:
            type = t
            format = ''
        fields[f]['type'] = type
        fields[f]['format'] = format
        fields[f]['null'] = n
        fields[f]['key'] = k
        fields[f]['default'] = d
        fields[f]['extra'] = e

    return fields

def oem_getfields(file):
    '''
    Get the fields from an OpenEdge table using 'table.dat' file
    '''

    fields = {}
    try:
        with open(file,'r') as f:
            lines = f.readlines()
    except Exception as e:
        print('Can not read file %s - %s' % (file,e))
        return False

    for line in lines:
        line = line.strip()
        tokens = line.split(';')
        fields[tokens[1]] = {}
        fields[tokens[1]]['type'] = tokens[2]
        fields[tokens[1]]['format'] = tokens[7]
        fields[tokens[1]]['extend'] = tokens[4]
        fields[tokens[1]]['default'] = tokens[5]
        fields[tokens[1]]['key'] = tokens[6]

    return fields

def compare_table(mdb, table, changename):
    '''
    Compare the table in both OpenEdge Database and MariaDB
    It will return a dictionary for each table
    '''
    compare = {}
    if table in changename:
        oetable = table
        mdbtable = table + '_'
    else:
        oetable = table
        mdbtable = table

    for f in oeschema[oetable].keys():
        if f in schema[mdb][mdbtable]:
            compare[f] = {}
            compare[f]['type'] = (oeschema[oetable][f]['type'],schema[mdb][mdbtable][f]['type'])
            compare[f]['format'] = (oeschema[oetable][f]['format'],schema[mdb][mdbtable][f]['format'])

    return compare


# Define parameters

parser = argparse.ArgumentParser(
        description="Query mariadb based on configfile"
        )
parser.add_argument('file',
        help="provide yaml based configfile"
        )
parser.add_argument('--loglevel', dest='loglevel', default='INFO',
        help='Provide loglevel (default is INFO)'
        )
parser.add_argument('--logfile', dest='logfile', default='getschema.log',
        help='Provide logfile (default is getschema.log)'
        )
parser.add_argument('--stage', dest='stage', default='../oeschema',
        help='Provide stage directory (default is ../oeschema)'
        )

args        = parser.parse_args()
config_file = args.file
loglevel    = args.loglevel.upper()
logfile     = args.logfile
stage       = args.stage

if not os.path.isdir(stage):
    print('Could not find directory %s - Exiting' % stage)
    sys.exit(1)

if __name__ == '__main__':

    if not loglevel in valid_loglevel:
        print('Invalid loglevel %s supplied - Exiting' % loglevel)
        sys.exit(1)

    '''
        Simple logging setup
    
    formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO, format=formatter, datefmt="[%X]", handlers=[logging.StreamHandler()]
    )
    '''

    ''' 
        More complex setup for logging
    '''

    # Setup logging
    logger = logging.getLogger(__name__)
    logger.setLevel(loglevel)

    # Logfile log output
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)  # Everything will be logged - based on logger.setLevel
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # Console log output
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)     # by default INFO or higher will be displayed
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='[%X]')
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    if not os.path.isfile(config_file):
        logger.error('File %s could not be found - Exiting' % config_file)
        sys.exit(1)
    
    try:
        with open(config_file, 'r') as file:
            cfg = yaml.safe_load(file)
    except PermissionError:
        logger.error('Not enough permissions to open file %s' % config_file)
        sys.exit(2)
    except Exception as e:
        logger.error('Failed to open file %s - %s' % (config_file, e))
        sys.exit(3)
    
    # Build schema for MariaDb
    schema = {}
    for db in ('o3_qaddb', 'o3_sysdb'):
        # Connect to MariaDB Platform
        conn = con_mariadb(cfg, db)
    
        # Built schema
        schema[db] = mdb_gettables(conn)
    
        for table in schema[db].keys():
            schema[db][table] = mdb_getfields(conn,table)
    
        logger.info('Number of tables (MariaDB %s): %d' % (db,len(schema[db].keys())))
        conn.close()
    
    '''
    print(json.dumps(schema, indent=3))
    for t in schema[cfg['database']].keys():
        print('\nFields for table %s:' % t)
        print(len('Fields for table %s:' % t)*'-')
        for f in schema[cfg['database']][t].keys():
            print('Field: %s' % f)
            print(len('Field: %s' % f)*'-')
            for k in schema[cfg['database']][t][f].keys():
                print('%s : %s' % (k,schema[cfg['database']][t][f][k]))
            print()
    
    '''
    
    # Verify tables from OpenEdge with MariaDB
    #dir = ('../stage_qadeam', '../stage_qadadm', '../stage_qaddb')
    dir = (stage,)
    
    schema_suffix = 'dat'
    index_suffix = 'idx'
    data_suffix = 'dump'
    
    # Get schema for OpenEdge (oe)
    oetables = []
    oeschema = {}
    for d in dir:
        oefiles = glob.glob(d + '/*.%s' % schema_suffix)
        for oefile in oefiles:
            fields = oem_getfields(oefile)
            oefile = oefile.split('/')[-1]
            oetables.append(oefile.split('.')[0])
            oeschema[oefile.split('.')[0]] = fields
    logger.info('Number of tables (OpenEdge databases): %d' % len(oeschema.keys()))
    
    notfound = []
    for oetable in oetables:
        found = False
        for db in ('o3_qaddb', 'o3_sysdb'):
            if oetable in schema[db]:
                found = True
        if found == False:
            notfound.append(oetable)
    
    changename = []
    for oetable in notfound:
        t = oetable + '_'
        for db in ('o3_qaddb', 'o3_sysdb'):
            if t in schema[db].keys():
                changename.append(oetable)
                break
    
    # Remove tables with changed names from notfound[]
    for t in changename:
        if t in notfound:
            notfound.remove(t)
    
    logger.info('Tables with changed names - %s' % changename)
    logger.info('Not found in MariaDB: %s' % notfound)
    
    # Verify OpenEdge tables with tables in MariaDB
    compare = {}
    for oetable in oeschema.keys():
        mdbtable = oetable
        if oetable in notfound:
            continue
        if oetable in schema['o3_qaddb']:
            mdbname = 'o3_qaddb'
        elif oetable in schema['o3_sysdb']:
            mdbname = 'o3_sysdb'
    
        compare[oetable] = compare_table(mdbname, oetable, changename)
    
        if oetable in changename:
            mdbtable = oetable + '_'
    
        for field in compare[oetable].keys():
            # Store data in variables
            oetype = compare[oetable][field]['type'][0]
            mdbtype = compare[oetable][field]['type'][1]
            oefmt = compare[oetable][field]['format'][0]
            mdbfmt = compare[oetable][field]['format'][1]
    
            # Check existence in MariaDB
            if not (int(oeschema[oetable][field]['extend']) > 0 or oeschema[oetable][field]['type'] == 'datetime-tz'):
                # Field is not an extent or is of datatype datetime-tz
                if not field in schema[mdbname][mdbtable].keys():
                    logger.warning('Field %s not found in %s.%s' % (field, mdbname, mdbtable))
    
            # Check for valid datatype conversion
            if not compare[oetable][field]['type'] in map_dt_oem_mdb:
                logger.warning('Field %s of %s.%s datatype issue - %s' % (field, mdbname, oetable, compare[oetable][field]['type']))
    
            # Check format
            if not oefmt == mdbfmt and not mdbtype in dt_no_fmt:
                # Differences in format
                if oetype == 'decimal':
                    if int(oefmt) > int(mdbfmt.split(',')[0]):
                        logger.warning('%s.%s.%s format issue - %s' % (mdbname, oetable, field, compare[oetable][field]['format']))
                elif int(oefmt) > int(mdbfmt):
                    logger.warning('%s.%s.%s format issue - %s' % (mdbname, oetable, field, compare[oetable][field]['format']))
    
    
    #print(json.dumps(compare['rpttmp_mstr'], indent=3))
