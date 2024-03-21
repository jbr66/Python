#!/usr/bin/python3
'''
NAME
    recordcount.py  -   Based on the dump files in the stage directory

AUTHOR
    Written by John Brink (j6b@qad.com)

USAGE

REVISION HISTORY
--------------------------------------------------
    0.1 03/15/2024  j6b - Initial start
--------------------------------------------------
vim:ts=4
'''

import glob
import sys
import mariadb
import argparse
from subprocess import Popen, PIPE


def connectMariadb(db):
    '''
    Connect to mariadb with static data
    '''
    try:
        conn = mariadb.connect(
            host="172.23.2.221",
            user="mfg",
            password="qad",
            db="%s" % db
        )
    except Exception as e:
        print('Failed to connect to mariadb - %s' % e)
        sys.exit(1)

    return conn


parser = argparse.ArgumentParser()
parser.add_argument('--stage', dest='stage', default='../stage_qaddb',
                    help='Location of the dumped data files (default: ../stage_qaddb')
parser.add_argument('--mdbname', dest='mdbname', default='qaddb',
                    help='Name of the MariaDB application instance (default: qaddb)')
parser.add_argument('--sysdbname', dest='sysdbname', default='sysdb',
                    help='Name of the MariaDB system instance (default: sysdb)')

args = parser.parse_args()

stage = args.stage
mdbname = args.mdbname
sysdbname = args.sysdbname

suffix = 'dump'
dumped_count = {}
loaded_count = {}

# Dumped data
try:
    file_list = glob.glob('%s/*%s' % (stage, suffix))
except Exception as e:
    print('Failed to build file_list - %s' % e)
    sys.exit(1)

for file in file_list:
    table = file.split('/')[-1].split('.')[0]
    try:
        cmd = '/usr/bin/wc -l ' + file
        p = Popen(cmd.split(), stdout=PIPE)
        data = p.communicate()[0].strip()

    except Exception as e:
        print('Failed to read %s - %s' % (file, e))
        continue

    if int(data.split()[0]) - 1 < 0:
        dumped_count[table] = 0
    else:
        dumped_count[table] = int(data.split()[0]) - 1

# Loaded data
for db in (mdbname, sysdbname):
    conn = connectMariadb(db)
    cur = conn.cursor()
    cur.execute('show tables')
    tables = cur.fetchall()
    for i in tables:
        qry = 'select count(*) as %s from %s.%s' % (i[0], db, i[0])
        cur = conn.cursor()
        cur.execute(qry)
        try:
            x = cur.fetchone()
            loaded_count[i[0]] = int(x[0])
        except Exception as e:
            print('Failed to query %s - %s' % (i[0], e))
    conn.close()

print('%-30s %8s %8s' % ('TableName', 'Dumped', 'Loaded'))
for t in dumped_count:
    if t in loaded_count and not dumped_count[t] == 0:
        if not dumped_count[t] == loaded_count[t]:
            print("%-30s %8d %8d" % (t, dumped_count[t], loaded_count[t]))

'''
for t in loaded_count:
    if t in dumped_count and not dumped_count[t] == 0:
        if not dumped_count[t] == loaded_count[t]:
            print("%-30s %8d %8d" % (t,dumped_count[t], loaded_count[t]))
'''
