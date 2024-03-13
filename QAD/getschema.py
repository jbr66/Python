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

def con_mariadb(cfg):
    '''
    Connect to MariaDb from configfile, will return the connection
    '''
    try:
        conn = mariadb.connect(
            user     = cfg['user'],
            password = cfg['password'],
            host     = cfg['host'],
            port     = cfg['port'],
            database = cfg['database']
        )
        return conn
    except mariadb.Error as e:
        print('Error connecting to MariaDB Platform %s' % e)
        sys.exit(1)

def get_tables(conn):
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

def get_fields(conn, table):
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

# Define parameters

parser = argparse.ArgumentParser(
        description="Query mariadb based on configfile"
        )
parser.add_argument('file',
        help="provide yaml based configfile"
        )

args        = parser.parse_args()
config_file = args.file
schema      = {}

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

# Connect to MariaDB Platform
conn = con_mariadb(cfg)

# Built schema
schema[cfg['database']] = get_tables(conn)

for table in schema[cfg['database']].keys():
    schema[cfg['database']][table] = get_fields(conn,table)

print(json.dumps(schema, indent=3))
'''
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

conn.close()
