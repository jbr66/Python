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
import argparse
import os, sys

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

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user     = cfg['user'],
        password = cfg['password'],
        host     = cfg['host'],
        port     = cfg['port'],
        database = cfg['database']
    )
except mariadb.Error as e:
    print('Error connecting to MariaDB Platform %s' % e)
    sys.exit(1)

# Define variables
schema = {}
tables = {}

# Get cursor
cur  = conn.cursor()

cur.execute('SHOW tables')

for t in cur:
    tables[t[0]] = {}

schema[cfg['database']] = tables
print('\nTables in %s' % cfg['database'])
print(20*'-')
for table in schema[cfg['database']].keys():
    fields = {}
    print('\t%s' % table)
    qry = 'describe %s' % table
    cur.execute(qry)
    for f, t, n, k, d, e in cur:
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
    schema[cfg['database']][table] = fields

print("\nFields for table countries:")
print(len('Fields for table countries:')*'-')
for f in schema[cfg['database']]['countries'].keys():
    print('Field: %s' % f)
    print(len('Field: %s' % f)*'-')
    for k in schema[cfg['database']]['countries'][f].keys():
        print('%s : %s' % (k,schema[cfg['database']]['countries'][f][k]))
    print()

conn.close()
