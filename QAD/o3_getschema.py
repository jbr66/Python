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

# Define parameters

parser = argparse.ArgumentParser(
        description="Query mariadb based on configfile"
        )
parser.add_argument('file',
        help="provide yaml based configfile"
        )

args        = parser.parse_args()
config_file = args.file

if not os.path.isfile(config_file):
    print('File %s could not be found - Exiting' % config_file)
    sys.exit(1)

try:
    with open(config_file, 'r') as file:
        cfg = yaml.safe_load(file)
except PermissionError:
    print('Not enough permissions to open file %s' % config_file)
    sys.exit(2)
except Exception as e:
    print('Failed to open file %s - %s' % (config_file, e))
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

    print('Number of tables (MariaDB %s): %d' % (db,len(schema[db].keys())))
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
dir = ('../stage_qadeam', '../stage_qadadm', '../stage_qaddb')

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
print('Number of tables (OpenEdge databases): %d' % len(oeschema.keys()))
print()

notfound = []
for oetable in oetables:
    found = False
    for db in ('o3_qaddb', 'o3_sysdb'):
        if oetable in schema[db]:
            found = True
    if found == False:
        notfound.append(oetable)

print('Not found in MariaDB: %s' % notfound)
for oetable in notfound:
    oetable = oetable + '_'
    for db in ('o3_qaddb', 'o3_sysdb'):
        if oetable in schema[db]:
            print('Found %s in %s' % (oetable, db))
