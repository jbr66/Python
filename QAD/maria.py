#!/usr/bin/python3
'''
Example connecting mariadb using Python

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
import os
import sys

# Define parameters

parser = argparse.ArgumentParser(
    description="Query mariadb based on configfile")
parser.add_argument('file',
                    help="provide yaml based configfile")

args = parser.parse_args()
config_file = args.file

if not os.path.isfile(config_file):
    print("File {} could not be found - Exiting".format(config_file))
    sys.exit(1)

try:
    with open(config_file, 'r') as file:
        cfg = yaml.safe_load(file)
except PermissionError:
    print("Not enough permissions to open file {}".format(config_file))
    sys.exit(2)
except Exception as e:
    print("Failed to open file {} - {}".format(config_file, e))
    sys.exit(3)

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=cfg['user'],
        password=cfg['password'],
        host=cfg['host'],
        port=cfg['port'],
        database=cfg['database']
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform {e}")
    sys.exit(1)

# Get cursor
cur = conn.cursor()

country = "Net%"
cur.execute("SELECT country_id, name, area from countries where name like ?", (country,))

print("Query on countries")
print(20 * '-')
for c, n, a in cur:
    print(f"CountryId: {c}, Name: {n}, Area: {a}")

cur.execute("SHOW tables")

print("\nTables in {}".format(cfg['database']))
print(20 * '-')
tables = []
for t in cur:
    print("\t{}".format(t[0]))
    tables.append(t)

print("\nFields per table:")
print(20 * '-')
for t in tables:
    tablename = t[0]
    print(tablename)
    print(len(tablename) * '-')
    sqlstat = "describe " + tablename
    cur.execute(sqlstat)
    for f, t, n, k, d, e in cur:
        print(f"\t{f} {t} {n} {k} {d} {e}")

conn.close()
