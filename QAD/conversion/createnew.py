#!/usr/bin/python3
'''
NAME
    createnew.py  -   Create new empty database

AUTHOR
    Written by John Brink (j6b@qad.com)

USAGE

REVISION HISTORY
--------------------------------------------------
    0.1 03/21/2024  j6b - Initial start
--------------------------------------------------
vim:ts=4
'''

import sys
import os
import mariadb
import argparse
from subprocess import run

cfg = {}
cfg['mdbuser'] = 'mfg'
cfg['mdbpassword'] = 'qad'
cfg['host'] = '172.23.2.221'


def connectMariadb(cfg, db):
    '''
    Connect to mariadb with static data
    '''
    try:
        conn = mariadb.connect(
            host=cfg['host'],
            user=cfg['mdbuser'],
            password=cfg['mdbpassword'],
            db="%s" % db
        )
    except Exception as e:
        print('Failed to connect to mariadb - %s' % e)
        return False

    return conn


def mdb_backup(cfg, mdbname, file, data: bool):
    '''
    Create a backup of mdbname into file
    '''
    if os.path.isfile(file):
        print('File %s already exists - Exiting with no action' % file)
        return False

    include_data = '-d'
    if data:
        include_data = ''
    cmd = 'mariadb-dump -u %s -p%s -h %s %s %s > %s' % (
        cfg['mdbuser'],
        cfg['mdbpassword'],
        cfg['host'],
        include_data,
        mdbname,
        file)

    try:
        result = run(cmd, shell=True)
        return result
    except Exception as e:
        print('Failed to run backup - %s' % cmd)
        print('Error: %s' % e)
        return False

    return True


def mdb_restore(cfg, new, old, file):
    '''
    Create new database instance from file
    '''
    if not os.path.isfile(file):
        print('Cannot find file %s - Exiting with no action' % file)
        return False

    conn = connectMariadb(cfg, old)
    if conn is False:
        print('Failed to connect to MariaDB - %s' % old)
        return False

    cur = conn.cursor()
    qry = 'CREATE DATABASE IF NOT EXISTS %s' % new

    result = cur.execute(qry)
    conn.close()

    cmd = 'mariadb -u %s -p%s -h %s %s < %s > /dev/null 2>&1' % (
        cfg['mdbuser'],
        cfg['mdbpassword'],
        cfg['host'],
        new,
        file)
    try:
        result = run(cmd, shell=True)
        return result
    except Exception as e:
        print('Failed to create %s - %s' % (new, e))
        return False


parser = argparse.ArgumentParser()
parser.add_argument('--sysdb', dest='sysdb', default='o3_sysdb',
                    help='Name of the MariaDB system instance (default: o3_sysdb)')
parser.add_argument('--newsysdb', dest='newsysdb', default='custsysdb3',
                    help='Name of the MariaDB system instance (default: custsysdb)')

args = parser.parse_args()

sysdb = args.sysdb
newsysdb = args.newsysdb
file = sysdb + '.sql'

result = mdb_backup(cfg, sysdb, file, False)
if not result:
    print('Failed to make a backup of %s' % sysdb)
    sys.exit(1)

result = mdb_restore(cfg, newsysdb, sysdb, file)
if not result:
    print('Failed to create %s' % newsysdb)
else:
    print('%s has been restored from %s' % (newsysdb, sysdb))
