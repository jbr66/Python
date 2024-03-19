#!/usr/bin/python3
'''
NAME
    validate.py    -   Validate schema, data, indexes and sequences

'''

import mariadb
# import yaml
# import json
# import argparse
# import sys
import os
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
    ('raw', 'varbinary'),]

'''
    DataType in MariaDB without format
'''

dt_no_fmt = [
    'text',
    'date',
    'mediumtext',
    'longblob',
    'timestamp',]

valid_loglevel = [
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL',]


def con_mariadb(cfg, mdb, logger):
    '''
    Connect to MariaDb mdb from configfile, will return the connection
    '''
    try:
        conn = mariadb.connect(
            user=cfg['mdbuser'],
            password=cfg['mdbpassword'],
            host=cfg['mdbhost'],
            port=cfg['mdbport'],
            database=mdb
        )
        return conn
    except mariadb.Error as e:
        logger.error('Error connecting to MariaDB Platform %s' % e)
        return False


def mdb_gettables(conn):
    '''
    Returns dictionary of tables
    '''

    tables = {}
    # Get cursor
    _cur = conn.cursor()

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


def mdb_getidxs(conn, mdb, table):
    '''
    Returns dictionary of indexes for given table
    '''

    indexes = {}
    idx = []
    # Get cursor
    _cur = conn.cursor()

    qry = 'show indexes from %s.%s' % (mdb, table)
    _cur.execute(qry)
    for t in _cur:
        idx.append(t)

    # Example: idx contains tupels of fields part of an index
    #  <table, <unique (1)>, <name idx>, <order>, <columname>, <collation>,
    #  <cardinality>, <sub_part>, <packed>, Null, <indexType>, <comment>,
    #  <indexcomment>, <ignored>
    # ('Posting', 1, 'idx__addglnbridx', 3, 'recid', 'A', 0, None, None, '',
    #  'BTREE', '', '', 'NO')
    if idx == []:
        return False

    for i in idx:
        if i[2] not in indexes.keys():
            indexes[i[2]] = {}
            indexes[i[2]][i[3]] = i[4]
        else:
            indexes[i[2]][i[3]] = i[4]

    # indexes will be something like below:
    # {'PRIMARY': {1: 'recid'},
    #  'idx__uniqueidx':
    #   {1: 'Company_ID', 2: 'PostingYear', 3: 'Journal_ID', 4: 'PostingVoucher'},
    #  'idx__prim':
    #   {1: 'Posting_ID'},
    #  'idx__addglnbr':
    #   {1: 'Company_ID', 2: 'PostingAddGLNbr', 3: 'PostingAddGLNbrDate', 4: 'recid'},
    #  'idx__addglnbridx': {1: 'Company_ID', 2: 'PostingAddGLNbrDate', 3: 'recid'}
    # }
    return indexes


def oem_getfields(file, logger):
    '''
    Get the fields from an OpenEdge table using 'table.dat' file
    '''

    fields = {}
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        logger.error('Can not read file %s - %s' % (file, e))
        return False

    for line in lines:
        line = line.strip()
        tokens = line.split(';')
        fields[tokens[1]] = {}
        fields[tokens[1]]['type'] = tokens[2]
        fields[tokens[1]]['format'] = tokens[7]
        fields[tokens[1]]['extend'] = tokens[4]
        fields[tokens[1]]['default'] = tokens[5]

    return fields


def oem_getidxs(file, logger):
    '''
    Get the indexes from an OpenEdge table using 'table.idx' file
    '''

    indexes = {}
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        logger.error('Can not read file %s - %s' % (file, e))
        return False

    for line in lines:
        line = line.strip()
        tokens = line.split(',')
        if tokens[0] not in indexes.keys():
            indexes[tokens[0]] = {}
            indexes[tokens[0]][tokens[1]] = tokens[3]
        else:
            indexes[tokens[0]][tokens[1]] = tokens[3]

    return indexes


def compare_table(schema, oeschema, table, changename):
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
        if f in schema[mdbtable]:
            compare[f] = {}
            compare[f]['type'] = (oeschema[oetable][f]['type'],
                                  schema[mdbtable][f]['type'])
            compare[f]['format'] = (oeschema[oetable][f]['format'],
                                    schema[mdbtable][f]['format'])

    return compare


def searchTable(cfg, oetables, schema, logger):
    '''
    Return arrays notfound[] and changename[]
    '''
    try:
        mdbqad = cfg['mdbname']
        mdbsys = cfg['mdbname_sys']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    notfound = []
    changename = []
    for oetable in oetables:
        found = False
        for db in (mdbqad, mdbsys):
            if oetable in schema[db]:
                found = True
        if found is False:
            notfound.append(oetable)

    changename = []
    for oetable in notfound:
        t = oetable + '_'
        for db in (mdbqad, mdbsys):
            if t in schema[db].keys():
                changename.append(oetable)
                break

    # Remove tables with changed names from notfound[]
    for t in changename:
        if t in notfound:
            notfound.remove(t)

    return notfound, changename


def collectfiles(cfg, logger, suffix):
    '''
    Collect the files from the stage directory based on suffix
    and will return an array of files (fysical files) and tables
    '''

    try:
        stage = cfg['stage']
        process_entire_database = eval(cfg['process_entire_database'])
        exclude_tables = cfg['exclude_tables']
        include_tables = cfg['include_tables']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False, False

    logger.info('reading from %s directory' % stage)

    if not os.path.isdir(stage):
        logger.error('Could not find directory %s - Exiting' % stage)
        return False, False

    files = []
    newfiles = []
    tables = []
    tablelist = []
    exclude_list = []

    if process_entire_database is False:
        tablelist = include_tables.split(',')
        logger.info('Validating only tables: %s' % ', '.join(tablelist))
    else:
        exclude_list = exclude_tables.split(',')

    files = glob.glob('%s/*.%s' % (stage, suffix))
    for file in files:
        table = file.strip().split('/')[-1].split('.')[0]
        if process_entire_database is True and table not in exclude_list:
            tables.append(table)
            newfiles.append(file)
        elif process_entire_database is False and table in tablelist:
            tables.append(table)
            newfiles.append(file)

    return newfiles, tables


def validateData(cfg, logger, operation):
    '''
    Validate schema and data
    '''

    # Console log output
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)     # by default DEBUG or higher will be displayed
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='[%X]')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    logger.info('*** %s ***' % operation)

    try:
        stage = cfg['stage']
        mdbqad = cfg['mdbname']
        mdbsys = cfg['mdbname_sys']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    # Collect files from 'stage' directory
    (oefiles, oetables) = collectfiles(cfg, logger, 'dat')

    # Build schema for MariaDb
    schema = {}
    for db in (mdbqad, mdbsys):
        # Connect to MariaDB Platform
        conn = con_mariadb(cfg, db, logger)
        if isinstance(conn, bool):
            if conn is False:
                return False

        # Built schema
        schema[db] = mdb_gettables(conn)

        for table in schema[db].keys():
            schema[db][table] = mdb_getfields(conn, table)

        conn.close()

    # Build schema for OpenEdge (oe)
    oeschema = {}
    for oefile in oefiles:
        table = oefile.split('/')[-1].split('.')[0]
        fields = oem_getfields(oefile, logger)
        if isinstance(fields, bool):
            if fields is False:
                return False
        oeschema[table] = fields

    (notfound, changename) = searchTable(cfg, oetables, schema, logger)

    # Verify OpenEdge tables with tables in MariaDB
    compare = {}
    nr_warnings = 0
    nr_errors = 0
    for oetable in oeschema.keys():
        if oetable in changename:
            mdbtable = oetable + '_'
        else:
            mdbtable = oetable
        if oetable in notfound:
            continue
        if mdbtable in schema[mdbqad]:
            mdbname = mdbqad
        elif mdbtable in schema[mdbsys]:
            mdbname = mdbsys

        compare[oetable] = compare_table(schema[mdbname], oeschema, oetable, changename)

        # Check number of fields
        if not len(oeschema[oetable]) == len(schema[mdbname][mdbtable]):
            if len(oeschema[oetable]) < len(schema[mdbname][mdbtable]):
                logger.warning('Number of fields are not the same for %s - (%d, %d)' %
                               (oetable, len(oeschema[oetable]),
                                len(schema[mdbname][mdbtable])))
                nr_warnings += 1
            else:
                logger.error('Number of fields in OE is larger than in MariaDB \
                             for %s (%d, %d)' % (oetable,
                                                 len(oeschema[oetable]),
                                                 len(schema[mdbname][mdbtable])))
                nr_errors += 1

        for field in compare[oetable].keys():
            # Store data in variables
            oetype = compare[oetable][field]['type'][0]
            mdbtype = compare[oetable][field]['type'][1]
            oefmt = compare[oetable][field]['format'][0]
            mdbfmt = compare[oetable][field]['format'][1]

            # Check existence in MariaDB
            if not (int(oeschema[oetable][field]['extend']) > 0 or
                    oeschema[oetable][field]['type'] == 'datetime-tz'):
                # Field is not an extent or is of datatype datetime-tz
                if field not in schema[mdbname][mdbtable].keys():
                    logger.error('Field %s not found in %s.%s' % (field, mdbname, mdbtable))
                    nr_errors += 1

            # Check for valid datatype conversion
            if not compare[oetable][field]['type'] in map_dt_oem_mdb:
                logger.warning('Field %s of %s.%s datatype issue - %s' % (
                    field, mdbname, oetable, compare[oetable][field]['type']))

            # Check format
            if not oefmt == mdbfmt and mdbtype not in dt_no_fmt:
                # Differences in format
                if oetype == 'decimal':
                    if int(oefmt) > int(mdbfmt.split(',')[0]):
                        logger.warning('%s.%s.%s format issue - %s' % (
                            mdbname, oetable, field, compare[oetable][field]['format']))
                        nr_warnings += 1
                elif int(oefmt) > int(mdbfmt):
                    logger.warning('%s.%s.%s format issue - %s' % (
                        mdbname, oetable, field, compare[oetable][field]['format']))
                    nr_warnings += 1

            # Check size
            if oetype == 'character' and int(oefmt) > 512:
                if mdbfmt == 'varchar':
                    logger.error('%s.%s.%s is character and width larger than \
                                 512, but type in MariaDB is varchar' %
                                 (mdbname, oetable, field))

    # Show summary
    for db in schema.keys():
        logger.info('Number of tables (MariaDB %s): %d' % (db, len(schema[db].keys())))
    logger.info('Number of validated tables from %s: %d' % (stage,
                                                            len(oeschema.keys())))
    if len(changename) > 0:
        logger.info('Tables with changed names: %s' % ', '.join(changename))
    if len(notfound) > 0:
        logger.info('Not found in MariaDB: %s' % ', '.join(notfound))
    logger.info('errors: %d warnings: %d' % (nr_errors, nr_warnings))

    # Turn off console logging
    logger.removeHandler(ch)

    # print(json.dumps(oeschema, indent=3))

    return True


def validateIndex(cfg, logger, operation):
    '''
    Validate indexes
    '''

    # Console log output
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)     # by default DEBUG or higher will be displayed
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='[%X]')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    logger.info('*** %s ***' % operation)

    try:
        mdbqad = cfg['mdbname']
        mdbsys = cfg['mdbname_sys']
        idxprefix = cfg['idxprefix']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    # Collect files from 'stage' directory
    (oefiles, oetables) = collectfiles(cfg, logger, 'idx')

    # Build schema for MariaDb
    schema = {}
    for db in (mdbqad, mdbsys):
        # Connect to MariaDB Platform
        conn = con_mariadb(cfg, db, logger)
        if isinstance(conn, bool):
            if conn is False:
                return False

        # Built schema
        schema[db] = mdb_gettables(conn)

    (notfound, changename) = searchTable(cfg, oetables, schema, logger)

    oeidx = {}
    mdbidx = {}
    nr_warnings = 0
    nr_errors = 0
    for oefile in oefiles:
        found = False
        oetable = oefile.split('/')[-1].split('.')[0]
        indexes = oem_getidxs(oefile, logger)
        if isinstance(indexes, bool):
            if indexes is False:
                return False
        oeidx[oetable] = indexes

        for db in (mdbqad, mdbsys):
            if oetable in changename:
                mdbtable = oetable + '_'
            else:
                mdbtable = oetable
            if mdbtable in schema[db]:
                mdbname = db
                found = True

        if found is True:
            mdbidx[mdbtable] = mdb_getidxs(conn, mdbname, mdbtable)

            # Check number of indexes
            if not len(oeidx[oetable].keys()) == len(mdbidx[mdbtable].keys()):
                logger.error('Number of indexes are not the same for %s (%d, %d)' %
                             (oetable, len(oeidx[oetable].keys()),
                              len(mdbidx[mdbtable].keys())))
                nr_warnings += 1

            # Check indexes
            for k in oeidx[oetable].keys():
                if k == 'FWDPRIMARY':
                    if 'PRIMARY' not in mdbidx[mdbtable].keys():
                        logger.error('Missing primary index for table %s' %
                                     oetable)
                        nr_errors += 1
                elif (idxprefix + k).lower() not in mdbidx[mdbtable].keys():
                    logger.warning('Missing index %s for table %s' % (k,
                                                                      oetable))
                    nr_errors += 1
        else:
            logger.warning('Table %s not found in MariaDB' % oetable)
            nr_warnings += 1

    # print(json.dumps(mdbidx, indent=3))
    # print(json.dumps(oeidx, indent=3))
    # print(json.dumps(schema[mdbsys], indent=3))
    logger.info('errors: %d warnings: %d' % (nr_errors, nr_warnings))

    # Turn off console logging
    logger.removeHandler(ch)

    return True
