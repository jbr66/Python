'''

OpenEdge CDC and ETL library for QAD to MariaDB
Project Inspiration

Written by Derek Bradley
Copyright QAD 2023

From Python 3.6, all dictionaries are insertion ordered

YOU MUST upgrade the mariadb library to >= 1.1

example
pip3.7 install mariadb==1.1.6

You must also: pip3.7 install jaydebeapi
You must also: pip3.7 install confluent_kafka
'''

# import sys
import os
# import re
# import subprocess
from subprocess import Popen, PIPE
import io
import glob
import tempfile
import mariadb
import jaydebeapi
import uuid
from datetime import datetime
from confluent_kafka import Consumer, KafkaError, Producer


def byteify(data, ignore_dicts=False):
    # if this is a unicode string, return its string representation
    if isinstance(data, str):
        # handle non breaking spaces, which the input data is littered with
        data = data.replace("'", " ")
        return (' '.join(data.split()))
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        if None in data:
            data = []  # just null it
        # return [_byteify(item, ignore_dicts=True) for item in data]
        return [byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            # _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            byteify(key, ignore_dicts=True): byteify(value, ignore_dicts=True)
            for key, value in data.items()
        }
    # if it's anything else, return it in its original form
    return data


'''
CDC FUNCTIONS
'''


def cdc_extent_fields(fld, cfg, logger):
    '''
        default - just return what we have
    '''
    try:
        extent_fields = cfg['extent_fields']
        extent_qad_charfld1 = cfg['extent_qad_charfld1']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return fld

    newfld = ''
    if fld in extent_fields:

        tokens = extent_fields.split(',')
        for line in tokens:
            if fld in line:
                c = 1
                fieldcount = int(line.split(';')[1])
                while c <= fieldcount:
                    newfld = newfld + fld + str(c) + ','
                    c = c + 1
                break

    if newfld == '':
        return fld, False
    else:
        # remove trailing comma
        newfld = newfld[:-1]
        return newfld, True


def cdc_extent_values(fld, k, cfg, logger):
    '''
        cdc - handle extent values
    '''
    newk = ''
    v = k.split(';')
    f = fld.split(',')
    c = 0
    for line in f:
        newk = newk + line + " = " + "'" + v[c] + "',"
        c = c + 1
    newk = newk[:-1]

    return newk


def cdc_extent_values_nq(fld, k, cfg, logger):
    '''
        cdc - do not quote
    '''
    newk = ''
    v = k.split(';')
    f = fld.split(',')
    c = 0
    for line in f:
        newk = newk + line + " = " + v[c] + ","
        c = c + 1
    newk = newk[:-1]

    return newk


def cdc_get_key(table, policyid, conn, logger):
    '''
        cdc - Get key
    '''
    key = ''

    try:
        keycurs = conn.cursor()
    except Exception as e:
        logger.error(f'Could not connect to cursor {e}')
        return False, False

    qry = 'select k."_field-position", k."_identifying-field" from PUB."_cdc-field-policy" k where k."_policy-id" = \'%s\' and k."_identifying-field" > \'0\' order by k."_identifying-field"' % (policyid)
    logger.info('Get Key Query %s' % qry)
    keycurs, result = run_oesql(conn, keycurs, qry, logger)
    if result is False:
        logger.error('Error getting key with %s' % qry)
        logger.error(result)
        key = ''

    for row in result:

        key = row
        break
        # will this ever have more than one row?  test

    # release cursor
    logger.info('close kcurs')
    keycurs.close()

    logger.info('key is %s' % type(key))

    return key


def cdc_get_sequence(conn, curs, table, logger):
    '''
        cdc - get sequence
    '''
    thisseq = 0

    qry = 'select cdc_table,cdc_sequence from PUB.cdc_det where cdc_table = \'%s\'' % (table)
    curs, result = run_oesql(conn, curs, qry, logger)

    if result is False:
        return thisseq

    for line in (list(result)):
        logger.info(line[1])
        thisseq = line[1]

    return thisseq


def cdc_get_mandatory(table, conn, mandatorydict, logger):
    '''
        cdc - get mandatory
    '''
    mlist = []

    '''
    we have non unique key fields marked as MANDATORY in the QAD schema.  This is pretty haphazard so we want to insert empty strings instead of NULLs on the fields that are mandatory.  Note that FWD simply ignores NULLs altogether and always inserts a default value.
    '''
    try:
        mcurs = conn.cursor()
    except Exception as e:
        logger.error(f'Could not connect to cursor {e}')
        return mandatorydict

    # like this :   select "_field-name" from pub."_field" WHERE "_mandatory" = 1 and "_file-recid" = (SELECT ROWID FROM pub."_file" WHERE "_file-name" = 'tr_hist') ;
    qry = 'select "_field-name" from pub."_field" WHERE "_mandatory" = 1 and "_file-recid" = (SELECT ROWID FROM pub."_file" WHERE "_file-name" = \'%s\')' % table

    mcurs, result = run_oesql(conn, mcurs, qry, logger)
    logger.info(f'Mandatory fields: {result}')
    if result is False:
        logger.error('Error getting mandatory fields with %s' % qry)
        logger.error(result)
        return mandatorydict

    for row in result:
        mlist.append(row[0])

    if mlist:
        mandatorydict[table] = mlist
    return mandatorydict


def cdc_get_tables(conn, tables, seq, cfg, logger):
    '''
        cdc - Get tables
    '''
    try:
        cdc_owner = cfg['cdc_owner']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    try:
        curs = conn.cursor()
    except Exception as e:
        logger.error(f'Could not connect to cursor {e}')
        return False, False

    qry = 'select f."_File-name", f."_File-number" from PUB."_File" f join PUB."_CDC-Table-Policy" tp on f.rowid = tp."_Source-File-Recid"'
    curs, result = run_oesql(conn, curs, qry, logger)

    curs.close()

    logger.info('sorting tables')
    result = sorted(list(result))

    for line in (list(result)):
        if result:
            tables[line[0]] = line[1]
            seq[line[0]] = 0

    count = 0
    for k, v in tables.items():
        logger.info(k)
        count = count + 1
        if count > 10:
            break

    return tables, seq


def cdc_push_add(changeseq, row, column_names, fieldmap, table, cdc_owner, p, key, conn, curs, cfg, logger, mandatorydict):
    '''
        cdc - push to add
    '''
    try:
        ncurs = conn.cursor()
    except Exception as e:
        logger.error(f'Could not connect to cursor {e}')
        return False

    try:
        quotefields = cfg['sql_quotefields']
        mandatory_to_not_null = cfg['mandatory_to_not_null']
        fwd_index_key = cfg['fwd_index_key']
        fwd_sequence = cfg['fwd_sequence']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    mlist = []
    try:
        mlist = mandatorydict[table]
    except Exception:
        logger.info('No mandatory fields for table %s' % table)

    # convert key to list
    keylist = list(key)
    logger.info(keylist)
    # identifying field + offset
    key = int(keylist[1] + 8)

    kstring = 'INSERT INTO %s (%s,' % (table, fwd_index_key)

    # first data field
    columncount = -1

    f = []
    fe = []
    fv = {}
    for k in row:
        columncount = columncount + 1
        # QAD fields start at 9
        if columncount < 9:
            continue

        if k is None:
            continue

        # Boolean
        if fieldmap[column_names[columncount]][0] == 'BOOLEAN':

            if k is False:
                k = '0'
            if k is True:
                k = '1'

        # skip empty strings if emptyToNull is True *UNLESS* the field is marked mandatory in OE schema
        if fieldmap[column_names[columncount]][0] == 'CHAR' and mandatory_to_not_null is False:
            # fwd mode, do nothing
            pass
        elif fieldmap[column_names[columncount]][0] == 'CHAR' and k == '':

            # empty string, but we still need to send it if the field is mandatory
            if column_names[columncount] in mlist:
                logger.info('found %s in mlist' % column_names[columncount])
                if not column_names[columncount] in f:
                    f.append(column_names[columncount])
                    fv[column_names[columncount]] = k
            else:
                # do not send empty string on non mandatory field
                continue
        else:
            if fieldmap[column_names[columncount]][0] == 'CHAR' and k != '':
                if not column_names[columncount] in f:
                    f.append(column_names[columncount])
                    fv[column_names[columncount]] = k
            elif fieldmap[column_names[columncount]][0] != 'CHAR':
                if not column_names[columncount] in f:
                    f.append(column_names[columncount])
                    fv[column_names[columncount]] = k

    # extents
    for line in f:

        result, foundExtent = cdc_extent_fields(line, cfg, logger)
        if foundExtent:
            v = result.split(',')
            i = fv[line].split(';')
            count = 0
            # remove the original field and add the extents
            del fv[line]
            for nv in v:
                fe.append(nv)
                fv[nv] = i[count]
                count = count + 1
        else:
            fe.append(result)

    for k, v in fv.items():
        kstring = kstring + k + ','
    kstring = kstring[:-1] + ' ) VALUES ( nextval(%s),' % fwd_sequence

    for k, v in fv.items():
        kstring = kstring + "'" + str(v) + "',"
    msg = kstring[:-1] + ' )'

    logger.info('MariaDb Kafka add -> %s ' % kstring)
    ncurs.close()

    result = cdc_send_kafka(cfg, changeseq, msg, p, table, logger)

    return result


def cdc_push_delete(changeseq, row, column_names, fieldmap, table, cdc_owner, p, key, conn, curs, cfg, logger):
    '''
        cdc - Push delete
    '''
    try:
        ncurs = conn.cursor()
    except Exception as e:
        logger.error(f'Could not connect to cursor {e}')
        return False

    try:
        quotefields = cfg['sql_quotefields']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    # convert key to list
    keylist = list(key)
    logger.info(keylist)
    # identifying field + offset
    key = int(keylist[1] + 8)

    kstring = 'DELETE FROM %s WHERE ' % table

    # first data field
    columncount = -1
    for k in row:
        columncount = columncount + 1
        # QAD fields start at 9
        if columncount < 9:
            continue

        if k is None:
            continue

        # skip empty strings
        if fieldmap[column_names[columncount]][0] == 'CHAR':
            if k == '':
                continue

        if columncount == key:
            logger.info('%s->%s->%s-->%d' % (column_names[columncount], fieldmap[column_names[columncount]][0], k, columncount))
            kstring = kstring + column_names[columncount] + ' = '

            # need to use the fieldmap to work out whether to quote the string
            if fieldmap[column_names[columncount]][0] in quotefields:
                kstring = kstring + "'" + str(k) + "',"
            else:
                if fieldmap[column_names[columncount]][0] == 'DECIMAL':
                    if 'e+' in str(k):
                        qry = 'select cast(%s as char(%d)) from %s.CDC_%s WHERE CDC_%s."_Change-sequence" = %d' % (curs.description[columncount][0], curs.description[columncount][2], cdc_owner, table, table, changeseq)
                        ncurs, result = run_oesql(conn, ncurs, qry, logger)
                        for n in result:
                            n = n[0].rstrip()

                            if 'oid' in curs.description[columncount][0]:
                                n = cdc_fix_oid(n, logger)
                            kstring = kstring + n + ','
                    else:
                        if len(str(k)) > 15:
                            if 'oid' in curs.description[columncount][0]:
                                k = cdc_fix_oid(k, logger)
                        kstring = kstring + str(f'{k:f}') + ','
                else:
                    kstring = kstring + str(k) + ','

    # strip last comma
    msg = kstring[:-1]
    logger.info('MariaDb Kafka delete -> %s ' % kstring)
    ncurs.close()

    result = cdc_send_kafka(cfg, changeseq, msg, p, table, logger)

    return result


def cdc_push_update(changeseq, row, column_names, fieldmap, table, cdc_owner, p, key, conn, curs, cfg, logger):

    try:
        ncurs = conn.cursor()
    except Exception as e:
        logger.error(f'Could not connect to cursor {e}')
        return False

    try:
        quotefields = cfg['sql_quotefields']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    # convert key to list
    keylist = list(key)
    logger.info(keylist)
    # identifying field + offset
    key = int(keylist[1] + 8)

    kstring = 'UPDATE %s SET ' % table

    # first data field
    columncount = -1
    for k in row:
        columncount = columncount + 1
        # QAD fields start at 9
        if columncount < 9:
            continue

        if k is None:
            continue

        if fieldmap[column_names[columncount]][0] == 'BOOLEAN':

            if k is False:
                k = '0'
            if k is True:
                k = '1'

        # skip empty strings
        if fieldmap[column_names[columncount]][0] == 'CHAR':
            if k == '':
                continue

        fld = column_names[columncount]
        fld, foundExtent = cdc_extent_fields(fld, cfg, logger)
        if foundExtent:
            logger.info('Found extent string %s' % fld)
        else:
            # kstring = kstring + column_names[columncount] + ' = '
            kstring = kstring + fld + ' = '
        logger.info('%s->%s->%s' % (column_names[columncount], fieldmap[column_names[columncount]][0], k))
        # need to use the fieldmap to work out whether to quote the string

        if fieldmap[column_names[columncount]][0] in quotefields:
            if foundExtent:
                k = cdc_extent_values(fld, str(k), cfg, logger)
                kstring = kstring + k + ","
            else:
                kstring = kstring + "'" + str(k) + "',"
        else:

            # handle arbitrary precision by casting to char
            # does not support arrays at this time
            if fieldmap[column_names[columncount]][0] == 'DECIMAL':
                if 'e+' in str(k):
                    qry = 'select cast(%s as char(%d)) from %s.CDC_%s WHERE CDC_%s."_Change-sequence" = %d' % (curs.description[columncount][0], curs.description[columncount][2], cdc_owner, table, table, changeseq)
                    ncurs, result = run_oesql(conn, ncurs, qry, logger)
                    for n in result:
                        n = n[0].rstrip()
                        if 'oid' in curs.description[columncount][0]:
                            n = cdc_fix_oid(n, logger)
                        kstring = kstring + n + ','
                else:
                    if foundExtent:
                        k = cdc_extent_values_nq(fld, str(k), cfg, logger)
                        kstring = kstring + k + ','
                    else:
                        kstring = kstring + str(f'{k:f}') + ','
            else:
                if foundExtent:
                    k = cdc_extent_values_nq(fld, str(k), cfg, logger)
                    kstring = kstring + k + ','
                else:
                    kstring = kstring + str(k) + ','

    # strip last comma
    kstring = kstring[:-1]
    # add bracket
    kstring = kstring + ' WHERE '

    columncount = -1
    for k in row:
        columncount = columncount + 1
        if columncount < 9:
            continue

        if columncount == key:
            logger.info('%s->%s->%s-->%d' % (
                column_names[columncount],
                fieldmap[column_names[columncount]][0],
                k, columncount))
            kstring = kstring + column_names[columncount] + ' = '

            # fix oid

            try:
                if column_names[columncount].split('_') == 'oid':
                    k = cdc_fix_oid(k, logger)
            except Exception:
                pass

            # need to use the fieldmap to work out whether to quote the string
            if fieldmap[column_names[columncount]][0] in quotefields:
                kstring = kstring + "'" + str(k) + "',"
            else:
                if fieldmap[column_names[columncount]][0] == 'DECIMAL':
                    if 'e+' in str(k):
                        qry = 'select cast(%s as char(%d)) from %s.CDC_%s WHERE CDC_%s."_Change-sequence" = %d' % (curs.description[columncount][0], curs.description[columncount][2], cdc_owner, table, table, changeseq)
                        ncurs, result = run_oesql(conn, ncurs, qry, logger)
                        for n in result:
                            n = n[0].rstrip()
                            if 'oid' in curs.description[columncount][0]:
                                n = cdc_fix_oid(n, logger)
                            kstring = kstring + n + ','
                    else:
                        if len(str(k)) > 15:
                            if 'oid' in curs.description[columncount][0]:
                                k = cdc_fix_oid(k, logger)
                            kstring = kstring + str(f'{k:f}') + ','
                else:
                    kstring = kstring + str(k) + ','

    # strip last comma
    msg = kstring[:-1]
    logger.info('MariaDb Kafka insert -> %s ' % kstring)
    ncurs.close()

    result = cdc_send_kafka(cfg, changeseq, msg, p, table, logger)

    return result


def cdc_send_kafka(cfg, changeseq, msg, p, table, logger):

    hdict = {}

    try:
        hdict['id'] = str(uuid.uuid4())
        hdict['source'] = cfg['kafka_headers']['source']
        hdict['specversion'] = str(cfg['kafka_headers']['specversion'])
        hdict['type'] = cfg['kafka_headers']['type']
        hdict['datacontenttype'] = cfg['kafka_headers']['datacontenttype']
        hdict['time'] = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        hdict['qadsrcdb'] = cfg['sql_db']
        hdict['qadsnkdb'] = cfg['kafka_headers']['qadsnkdb']
        hdict['qadenvtype'] = cfg['kafka_headers']['qadenvtype']
        hdict['qadsequence'] = str(changeseq)
        hdict['host'] = cfg['sql_host']
        hdict['table'] = table
        send_topic = cfg['send_topic']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e} Cannot produce Kafka Message')
        return False

    try:
        logger.info('Producing %s' % msg)

        p.produce(send_topic, value=bytes(str(msg).encode()), key='', headers=hdict)

    except Exception as e:
        logger.error(e)
        return False

    logger.info('Successfully produced')
    return True


def cdc_sequence_start(conn, seq, cfg, logger):

    try:
        cdc_owner = cfg['cdc_owner']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    try:
        curs = conn.cursor()
    except Exception as e:
        logger.error(f'Could not connect to cursor {e}')
        # return False, False
        return False

    qry = 'select cdc_table, cdc_sequence from PUB.cdc_det'
    curs, result = run_oesql(conn, curs, qry, logger)

    curs.close()

    logger.info('Sequences --> ')
    for line in (list(result)):
        logger.info(line)
        seq[line[0]] = line[1]

    return seq


def cdc_track_changes(conn, curs, p, table, keys, tn, seq, cfg, mandatorydict, logger):
    '''
    field map :
      _policy-id, _operation, _tran-id, _time-stamp, _change-sequence, _continuation_position, _arrayindex, _fragment
    '''
    logger.debug('Tracking %s' % table)

    first = 0
    count = 0
    try:
        cdc_owner = cfg['cdc_owner']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    # refresh sequence value for table
    try:
        chgseq = seq[table]
    except KeyError as e:
        logger.warning(f'Cannot find change sequence start value for %s {e}' % table)
        chgseq = 0

    if chgseq > 0:
        logger.info('checking sequence current value for %s' % table)

        chgseq = cdc_get_sequence(conn, curs, table, logger)
        logger.info('seq = %d' % chgseq)

    initchgseq = chgseq
    logger.debug('looking for changes on %s' % tn)

    qry = 'select ct."_policy-id",ct."_operation",c.* from PUB."_cdc-change-tracking" ct inner join %s.CDC_%s c ON ct."_Change-sequence" = c."_Change-sequence" where ct."_Change-Sequence" > %d and ct."_Source-Table-Number" = %s order by ct."_Source-Table-Number", ct."_Change-Sequence"' % (cdc_owner, table, chgseq, tn)
    curs, result = run_oesql(conn, curs, qry, logger)
    if result is False:
        logger.error('ERROR running extraction')
        return (seq, keys)
    else:
        # column_names = [table + '.' + i[0] for i in curs.description]
        # column_types = [i[1].values[0] for i in curs.description]
        # fieldmap = dict(zip(column_names, column_types))

        for row in result:

            if count == 0:
                # column_names = [table + '.' + i[0] for i in curs.description]
                column_names = [i[0] for i in curs.description]
                column_types = [i[1].values for i in curs.description]
                fieldmap = dict(zip(column_names, column_types))
                logger.info('Changes Found')
                logger.info(fieldmap)

                # does key exist from field policies?  if not, go get it.  key needed for deletes and updates.
                # Note that we assume that every table has a key, so at this point if we are getting a new key, we can go and grab the mandatory fields as well
                try:
                    key = keys[table]
                except Exception as e:
                    logger.warning(e)
                    policyid = row[0]
                    logger.warning('key not found for %s , searching field policies to add using policy id %s' % (table, policyid))
                    key = cdc_get_key(table, policyid, conn, logger)
                    logger.warning('inserting into keys[]')
                    keys[table] = key
                    logger.info('refreshing mandatory fields for %s' % table)
                    mandatorydict = cdc_get_mandatory(table, conn, mandatorydict, logger)
                    if mandatorydict == {}:
                        logger.error('Could not load mandatory fields. SQL inserts may fail')

            count = count + 1
            operation = row[8]
            changeseq = row[4]

            logger.info('Operation is %s' % operation)
            # if operation is add

            if operation == 1:
                pushresult = cdc_push_add(
                    changeseq,
                    row,
                    column_names,
                    fieldmap,
                    table,
                    cdc_owner,
                    p,
                    key,
                    conn,
                    curs, cfg, logger, mandatorydict)

            if operation == 2:
                pushresult = cdc_push_delete(
                    changeseq,
                    row,
                    column_names,
                    fieldmap,
                    table,
                    cdc_owner,
                    p,
                    key,
                    conn,
                    curs, cfg, logger)

            if operation == 4:
                pushresult = cdc_push_update(
                    changeseq, row, column_names, fieldmap, table, cdc_owner, p, key, conn, curs, cfg, logger)

        # finally update cdc_det with correct change sequence for the table

        if count == 0:

            return (seq, keys)

        else:
            logger.info('final change sequence is %d initial was %d' % (
                changeseq, initchgseq))
            if initchgseq < changeseq:

                # does record exist?
                qry = 'select cdc_sequence from PUB.cdc_det WHERE cdc_table = \'%s\'' % (table)
                curs, result = run_oesql(conn, curs, qry, logger)
                if len(result) == 0:
                    logger.info('no record')

                    qry = 'insert into PUB.cdc_det ( cdc_table, cdc_sequence ) VALUES (  \'%s\' , %d )' % (table, changeseq)
                else:
                    qry = 'update PUB.cdc_det set cdc_sequence = \'%d\' where cdc_table = \'%s\'' % (changeseq, table)

                logger.info('Upsert sequence query : %s' % qry)
                curs, result = run_oesql_update(conn, curs, qry, logger)
                if result is False:
                    logger.error('ERROR UPDATING cdc_det ( trying to store updated change sequence with query %s' % qry)

            return (seq, keys)

    return (seq, keys)


def cdc_fix_oid(val, logger):

    logger.info('fixing oid %s' % val)
    if len(val) < 15:
        return val

    val = str(val)
    val = val[8:]
    val = val.lstrip('0')

    return val


def conn_kafka_producer(cfg, logger):
    '''
    Connect to Kafka
    '''

    try:
        kafka_bootstrap = cfg['kafka_bootstrap']
        client_id = cfg['sql_host']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    logger.info('connecting to %s' % (kafka_bootstrap))
    try:
        p = Producer({'bootstrap.servers': kafka_bootstrap, 'client.id': client_id})
    except KafkaError as e:
        logger.error(f'Kafka Error {e}')
        return False

    return p


def conn_mariadb(cfg, logger):
    '''
    Connect to MariaDB
    '''

    try:
        user = cfg['mdbuser']
        password = cfg['mdbpassword']
        host = cfg['mdbhost']
        port = cfg['mdbport']
        dbname = cfg['mdbname']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    try:
        conn = mariadb.connect(
            host="%s" % host,
            db="%s" % dbname,
            user="%s" % user,
            password="%s" % password,
            port=port)
    except mariadb.Error as e:
        print('Could not connect to MariaDB database host=%s db=%s user=%s password=#### port=%s ' % (host, dbname, user, port))
        print(e)
        return False

    return conn


def conn_oesql(cfg, logger):

    try:
        driverstring = cfg['driverstring']
        initstring = cfg['initstring']
        dlc = cfg['dlc'] + '/java/openedge.jar'
        service = cfg['sql_port']
        db = cfg['sql_db']
        hostname = cfg['sql_host']

        credentials = []
        credentials.append(cfg['sql_user'])
        credentials.append(cfg['sql_pass'])

        connstring = "jdbc:datadirect:openedge://%s:%s;DatabaseName=%s[-mdbq:alldb]" % (hostname, service, db)

    except KeyError:
        logger.error(f'YAML file is missing key {e}')
        return False

    logger.info('Connecting to OE using %s' % connstring)
    conn = jaydebeapi.connect(
        driverstring,
        connstring,
        credentials,
        dlc)
    logger.info(conn)

    return conn


def is_writeable(directory, logger):
    logger.info('Checking if directory %s is writeable' % directory)

    try:
        testfile = os.path.join(directory, 'testfile')
        with open(testfile, 'w') as f:
            f.write('test')
        os.remove(testfile)
        return True
    except Exception as e:
        return False


def extract(cfg, logger, operation):
    '''
    Extract

     this is a custom format that is more easily parsed than the legacy openedge .d format

     data is dumped to cfg['stage']

    '''

    logger.info('*** %s ***' % operation)

    try:
        stage = cfg['stage']
        process_entire_database = cfg['process_entire_database']
        exclude_tables = cfg['exclude_tables']
        include_tables = cfg['include_tables']
        oedbpath = cfg['oedbpath']
        oedbname = cfg['oedbname']
        abl = cfg[operation]
        quit_on_table_error = cfg['quit_on_table_error']
        large_clob_tables = cfg['large_clob_tables']
        fwd_index_name = cfg['fwd_index_name']
        fwd_index_key = cfg['fwd_index_key']
        fwd_index_field = cfg['fwd_index_field']
        fwd_sequence = cfg['fwd_sequence']
        datetime_index_suffix = cfg['datetime_index_suffix']
        reserved_suffix = cfg['reserved_suffix']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    logger.info('Extracting to %s directory' % stage)
    if not is_writeable(stage, logger):
        logger.error('Cannot write to %s' % stage)
        return False

    query = readdotp(abl, cfg, logger)
    if query is False:
        return False

    if process_entire_database is True:
        logger.info('Extracting all tables except %s from %s/%s' % (
            exclude_tables, oedbpath, oedbname))
        tablelist = tablewrapper(cfg, logger)
        if tablelist is False:
            logger.error('Cannot get the list of tables.  Exiting.')
            return False
    else:
        tablelist = include_tables.split(',')

    logger.info('Extracting %s from %s/%s' % (
        tablelist, oedbpath, oedbname))

    for table in tablelist:
        logger.info('Processing table %s' % table)
        tablequery = query.replace('#TABLE#', table)
        tablequery = tablequery.replace('#PATH#', stage)
        tablequery = tablequery.replace('#LARGECLOB#', large_clob_tables)
        tablequery = tablequery.replace('#FWD#', fwd_index_field)
        tablequery = tablequery.replace('#FWD_INDEX_NAME#', fwd_index_name)
        tablequery = tablequery.replace('#FWD_INDEX_KEY#', fwd_index_key)
        tablequery = tablequery.replace('#FWD_SEQUENCE#', fwd_sequence)
        tablequery = tablequery.replace('#SUFFIX#', reserved_suffix)
        tablequery = tablequery.replace('#OFFSET#', datetime_index_suffix)
        result = runabl(tablequery, cfg, logger)
        if result == False:
            logger.error('Could not extract %s for %s.  Skipping' % (
                operation, table))
            if quit_on_table_error:
                logger.info('quit_on_table_error is True. Exiting')
                return False
        else:
            logger.info('%s extracted for %s' % (operation, table))

        if operation == 'extractSchema':
            result = postprocessSchema(table, cfg, logger)
            if result is False:
                if quit_on_table_error:
                    logger.info('quit_on_table_error is True. Exiting')
                    return False

    return True


def extractSequence(cfg, logger, operation):

    logger.info('*** %s ***' % operation)

    try:
        stage = cfg['stage']
        oedbpath = cfg['oedbpath']
        oedbname = cfg['oedbname']
        abl = cfg[operation]
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    logger.info('Extracting to %s directory' % stage)
    if not is_writeable(stage, logger):
        logger.error('Cannot write to %s' % stage)
        return False

    query = readdotp(abl, cfg, logger)
    # if type(query) == bool:
    if isinstance(query, bool):
        if query is False:
            return False

    query = query.replace('#PATH#', stage)
    query = query.replace('#DBNAME#', oedbname)
    result = runabl(query, cfg, logger)
    if result is False:
        logger.error('Could not extract Sequences')
        return False

    return True


def load(cfg, logger, operation, conn):
    '''
    Load

     data is dumped to cfg['stage']

     We do not run through a table list from the source database as that database may not be on this server
     So we processes each file in the directory that meets our filter criteria.  If it is index or data we are loading we check the table exists first

     The mariaDB connection cursor must be passed in

    '''

    logger.info('*** %s ***' % operation)

    try:
        stage = cfg['stage']
        process_entire_database = cfg['process_entire_database']
        exclude_tables = cfg['exclude_tables']
        include_tables = cfg['include_tables']
        quit_on_table_error = cfg['quit_on_table_error']
        large_clob_tables = cfg['large_clob_tables']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    logger.info('reading from %s directory' % stage)

    suffix = None
    if operation == 'loadSchema':
        suffix = '.dat'
    if operation == 'loadIndex':
        suffix = '.idx'
    if operation == 'loadData':
        suffix = '.dump'

    if suffix is None:
        logger.error('Invalid operation %s.  Check process_functions in YAML config for spelling mistakes')
        return False

    file_list = glob.glob('%s/*%s' % (stage, suffix))
    file_list.sort()

    for file in file_list:
        table = file.split('.')[0].split('/')[-1]

        if "CDC_" in table:
            continue

        processFile = False
        if process_entire_database is True:
            excludeTable = False
            for exclude in exclude_tables.split(','):

                if exclude == table:
                    excludeTable = True
                    break

            if excludeTable is True:
                logger.info('Skipping Excluded table %s' % file)
                continue

            processFile = True

        else:

            for includetable in include_tables.split(','):
                if includetable == table:
                    processFile = True
                    break

        if processFile is True:
            logger.info('Processing %s' % (file))
            # process File
            if operation == 'loadSchema':
                result = loadSchema(file, cfg, logger, conn)
                if result is False:
                    return False
            if operation == 'loadIndex':
                result = loadIndex(file, table, cfg, logger, conn)
                if result is False:
                    return False
            if operation == 'loadData':
                result = loadData(file, table, cfg, logger, conn)
                if result is False:
                    return False

    return True


def loadData(fn, table, cfg, logger, conn):
    '''
    for loads we should set autocommit=0, SQL DML, commit, set autocommit=1
    also cfg driven
    run batches and commit after each batch cfg[commit_batch] ... load the queries into a list and then commit all queries in the list, emptying afterwards
    If loading data into a new MySQL instance, consider disabling redo logging using ALTER INSTANCE {ENABLE|DISABLE} INNODB REDO_LOG syntax. Disabling redo logging helps speed up data loading by avoiding redo log writes.  cfg[disable_redo_log]
    To use LOAD DATA INFILE wiih MySQL RDS on AWS, you need to enable the option to allow loading data from local files. You can do this by following these steps:

     Go to the AWS Management Console and open the RDS console.
     Select your MySQL RDS instance.
     Click on the "Configuration" tab.
     Scroll down to the "Additional Configuration" section.
     Select the "Allow loading data from local files" checkbox.
     Click on the "Save" button.
    '''

    logger.info('Load data from %s into %s' % (fn, table))

    qrylist = []
    reserved_words_dict = {}
    is_system_table = {}
    logger.info('*')
    try:
        mdbname = cfg['mdbname']
        fwd_index_name = cfg['fwd_index_name']
        large_clob_tables = cfg['large_clob_tables']
        mandatory_to_not_null = cfg['mandatory_to_not_null']
        stop_on_duplicate = cfg['stop_on_duplicate']
        stop_on_error = cfg['stop_on_error']
        require_empty_table = cfg['require_empty_table']
        skip_table_with_data = cfg['skip_table_with_data']
        fwd_index_key = cfg['fwd_index_key']
        fwd_sequence = cfg['fwd_sequence']
        encoding = cfg['encoding']
        reserved_words = cfg['reserved_words']
        reserved_suffix = cfg['reserved_suffix']
        system_tables = cfg['sys_tables']

        for line in reserved_words.split(','):
            reserved_words_dict[line] = 1
        for line in system_tables.split(','):
            line_upper = str.upper(line)
            is_system_table[line_upper] = 1

    except Exception as e:
        logger.error(e)
        return False

    # Verify if table is system table
    table_upper = str.upper(table)
    if table_upper in is_system_table:
        try:
            mdbname = cfg['mdbname_cust']
        except Exception as e:
            logger.error(e)
            return False

    if not os.path.isfile(fn):
        logger.error('dump file %s cannot be found' % fn)
        return False

    try:
        if os.stat(fn).st_size == 0:
            logger.info('zero size file %s.  No data' % fn)
            return True
    except Exception as e:
        logger.error(e)
        return False

    # table exists?
    try:
        exists = tableExists(table, mdbname, cfg, conn, logger)
    except Exception as e:
        logger.error('Cannot determine if table %s exists in %s' %
                     (table, mdbname))
        logger.error(e)
        return False

    if not exists:
        logger.error('%s DOES NOT exist in %s -- cannot load data' %
                     (table, mdbname))
        # do not exit program, continue on
        return True
    else:
        logger.info('Table %s found in database' % table)

    if require_empty_table is True:
        logger.info('Checking for empty table')
        qry = "SELECT EXISTS ( SELECT %s from %s.%s limit 1)" % (
            fwd_index_key, mdbname, table)
        cur = run_msql(qry, conn, cfg, logger)

        if cur is False:
            logger.info('Cannot read row count from %s.%s' % (
                mdbname, table))
            return False
        rows = cur.fetchone()
        if rows[0] == True:
            if skip_table_with_data == True:
                logger.error('Skipping to next table')
                return True

            logger.error('Data found in %s and require_empty_table is True.  Exiting' % table)
            return False
        cur.close()

    # ok we are ready to go
    first = True

    # this has weird logic because we need to handle corrupt unicode data from the openedge database
    # particularly invalid continuation bytes in double-byte languages like Chinese
    with io.open(fn, 'rb') as f:
        for line in f:
            try:
                line = line.decode('utf=8')

                if first is True:
                    # read schema
                    fields = line.strip().replace('^', ',')[:-1]
                    first = False
                    break

            except Exception as e:
                logger.error(e)
                logger.error('Cannot parse dump file %s exception type %s' % (fn, type(e)))
                continue

    # Now we need to replace any columns in the header that are reserved words
    newfields = []
    for token in fields.split(','):
        try:
            t = str.upper(token)

            dummy = reserved_words_dict[t]
            newfields.append(token + reserved_suffix)
            logger.info('Replacing reserved word %s with %s%s' % (
                token, token, reserved_suffix))

        except Exception as e:
            newfields.append(token)

    fields = ','.join(newfields)

    qry = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s.%s FIELDS TERMINATED BY '^' ignore 1 lines (%s) set %s = nextval(%s)" % (
        fn, mdbname, table, fields, fwd_index_key, fwd_sequence)
    # remove last comma

    logger.info(qry)

    cur = run_msql(qry, conn, cfg, logger)

    if cur == False:
        logger.info('Errors loading dump file for %s.%s' % (
            mdbname, table))
        if stop_on_error:
            return False
        else:
            logger.info('stop_on_error is False so we continue ...')
            return True
    warnings = conn.show_warnings()
    try:
        for warning in warnings:
            logger.warning(warning)
    except Exception:
        pass
    # we need to commit this load infile as it runs with autocommit off
    conn.commit()

    result = postprocessData(mdbname, table, cfg, conn, logger)
    return result


def loadIndex(fn, table, cfg, logger, conn):
    '''
    for loads we should set autocommit=0, SQL DML, commit, set autocommit=1
    '''

    logger.info('Load Index from %s into %s' % (fn, table))
    qrylist = []
    keys = 0

    reserved_words_dict = {}
    is_system_table = {}
    try:
        mdbname = cfg['mdbname']
        fwd_index_name = cfg['fwd_index_name']
        reserved_words = cfg['reserved_words']
        reserved_suffix = cfg['reserved_suffix']
        max_keys = int(cfg['max_keys'])
        system_tables = cfg['sys_tables']

        for line in reserved_words.split(','):
            reserved_words_dict[line] = 1
        for line in system_tables.split(','):
            line_upper = str.upper(line)
            is_system_table[line_upper] = 1

    except Exception as e:
        logger.error(e)
        return False

    # Verify if table is system table
    table_upper = str.upper(table)
    if table_upper in is_system_table:
        try:
            mdbname = cfg['mdbname_cust']
        except Exception as e:
            logger.error(e)
            return False

    # read structure from disk
    try:
        f = open(fn, 'r')
        content = f.readlines()
    except Exception as e:
        logger.error(e)
        return False
    f.close()

    # table exists?
    try:
        exists = tableExists(table, mdbname, cfg, conn, logger)
    except Exception as e:
        logger.error('Cannot determine if table %s exists in %s' % (table, mdbname))
        logger.error(e)
        return False

    if not exists:
        logger.error('%s DOES NOT exist -- cannot load index' % table)
        # do not exit program, continue on
        return True

    qryline = ''
    indexname = ''
    for line in content:
        if ',1,' in line:
            keys = keys + 1
        if keys >= max_keys:
            logger.error('total keys defined > %d on table %s so not adding any more' % (max_keys, table))
            break
        try:
            tokens = line.strip().split(',')

            # reserved word check ( index name )
            try:
                t = str.upper(tokens[0])
                dummy = reserved_words_dict[t]
                logger.info('Replacing reserved word %s with %s%s' % (
                    tokens[3], tokens[3], reserved_suffix))

                tokens[0] = tokens[0] + reserved_suffix
            except Exception as e:
                pass

            # reserved word check ( fields )
            try:
                t = str.upper(tokens[3])
                dummy = reserved_words_dict[t]
                logger.info('Replacing reserved word %s with %s%s' % (
                    tokens[3], tokens[3], reserved_suffix))

                tokens[3] = tokens[3] + reserved_suffix

            except Exception as e:
                pass

            # get ride of dashes
            tokens[0] = tokens[0].replace('-', '_')

            if tokens[0] == fwd_index_name:
                qrylist.append('ALTER TABLE %s.%s ADD CONSTRAINT %s PRIMARY KEY (%s)' % (
                    mdbname, table, fwd_index_name, tokens[3]))
            else:

                if tokens[2] == 'u':
                    unique = 'UNIQUE'
                else:
                    unique = ''

                if tokens[0] != indexname:
                    # remove last comma
                    if qryline.strip() != '':

                        qryline = qryline[:-1] + ')'
                        qrylist.append(qryline)
                        qryline = ''

                if tokens[1] == '1':
                    qryline = 'CREATE %s INDEX %s ON %s.%s ( %s ' % (
                        unique, tokens[0], mdbname, table, tokens[3]) + ','
                    indexname = tokens[0]
                else:
                    qryline = qryline + tokens[3] + ','

        except Exception as e:
            logger.error(e)
            return False

    # handle last index
    if qryline.strip() != '':
        qryline = qryline[:-1] + ')'
        qrylist.append(qryline)

    # check fields and remove any that are type text
    qrylist = loadIndexTextFieldCheck(qrylist, mdbname, table, conn, cfg, logger)
    if qrylist is False:
        logger.error('Cannot check database fields against the specified index fields')
        return False

    # for line in querylist run qry
    logger.info('this is the index list')
    logger.info(qrylist)

    for qry in qrylist:
        cur = run_msql(qry, conn, cfg, logger)
        if isinstance(cur, bool):
            if cur is False:
                return False

    return True


def loadIndexTextFieldCheck(qrylist, mdbname, table, conn, cfg, logger):
    '''
    check the definition of each field.
    If it is a text or mediumtext field, then drop it
    '''

    typedict = {}
    lengthdict = {}
    newqrylist = []

    try:
        max_index_length = cfg['max_index_length']
        default_byte_pad = cfg['default_byte_pad']
    except Exception as e:
        logger.error(e)
        return False

    qry = 'Show Columns from %s.%s' % (mdbname, table)
    cur = run_msql(qry, conn, cfg, logger)
    for line in cur:
        typedict[line[0]] = line[1].split('(')[0]
        try:

            val = line[1].split('(')[1].split(')')[0]
            if ',' in val:
                # handle decimal
                val = val.split(',')[0]

                lengthdict[line[0]] = val
        except Exception:
            lengthdict[line[0]] = default_byte_pad

    for line in qrylist:
        newfields = ''
        fieldlength = 0
        fields = line.split('(')[1].split(')')[0].split(',')
        for field in fields:
            field = field.strip()
            fieldlength = fieldlength + int(lengthdict[field])
            if fieldlength > int(max_index_length):
                logger.error('Dropping all fields past ( and including ) %s due to length restrictions for index %s ' % (field, line))
                break
            try:
                ftype = typedict[field]
                if ftype != 'text':
                    newfields = newfields + field + ','
                else:
                    logger.error('Removing field %s from Index %s' % (field, line))
            except Exception:
                pass

        newfields = newfields.strip()
        if newfields != '':
            newfields = newfields[:-1]
            newqry = line.split('(')[0] + '(' + newfields + ')' + line.split(')')[1]
            newqrylist.append(newqry)

    return newqrylist


def loadSchema(fn, cfg, logger, conn):
    '''
    for loads we should set autocommit=0, SQL DML, commit, set autocommit=1
    '''

    logger.info('Load Schema from %s' % fn)
    is_system_table = {}

    try:
        drop_table_if_exists = cfg['drop_table_if_exists']
        mdbname = cfg['mdbname']
        dropquery = "DROP TABLE IF EXISTS"
        mandatory_to_not_null = cfg['mandatory_to_not_null']
        system_tables = cfg['sys_tables']
        is_customer_owned = cfg['cust_owned_field']

        for line in system_tables.split(','):
            line_upper = str.upper(line)
            is_system_table[line_upper] = 1

    except Exception as e:
        logger.error(e)
        return False

    # read structure from disk
    try:
        f = open(fn, 'r')
        content = f.readlines()
        table = content[0].split(';')[0]
        logger.info('Table is %s' % table)

    except Exception as e:
        logger.error(e)
        return False
    f.close()

    # Verify if table is system table
    table_upper = str.upper(table)
    if table_upper in is_system_table:
        try:
            mdbname = cfg['mdbname_cust']
        except Exception as e:
            logger.error(e)
            return False

    # table exists?
    try:
        exists = tableExists(table, mdbname, cfg, conn, logger)
    except Exception as e:
        logger.error('Cannot determine if table %s exists in %s' %
                     (table, mdbname))
        logger.error(e)
        return False

    if exists:
        logger.info('%s exists' % table)
    else:
        logger.info('%s DOES NOT exist' % table)

    # drop?
    if drop_table_if_exists is True and exists:

        logger.info('Dropping table %s' % table)
        qry = dropquery + ' ' + mdbname + '.' + table

        cur = run_msql(qry, conn, cfg, logger)
        cur.close()
        # TODO Check result
        try:
            drop = tableExists(table, mdbname, cfg, conn, logger)
            if drop:
                logger.info('%s could not be dropped' % table)
                return False
        except Exception as e:
            logger.error('Failed to verify if table %s has been dropped from %s' % (table, mdbname))
            logger.error(e)
            return False

    elif exists:
        logger.error('Table %s exists so cannot continue loading schema' % table)
        return False

    # setup query
    qry = 'CREATE TABLE %s.%s  ( ' % (mdbname,table)

    for line in content:
        line = line.strip()
        if line == '':
            continue

        tokens = line.split(';')

        try:
            fieldname = tokens[1]
            fieldtype = tokens[2]
            fieldformat = tokens[3]
            fieldinitial = tokens[5]
            fieldmandatory = tokens[6]
            fieldwidth = tokens[7]
        except KeyError as e:
            logger.error('There is a problem with the format of the schema file')
            logger.error(e)
            return False

        nullable = ''
        if fieldmandatory == 'yes':
            if mandatory_to_not_null:
                logger.info('Setting %s to NOT NULL ( mandatory_to_not_null = True in cfg )' %
                            (fieldname))
                nullable = ' NOT NULL '

        fieldtype = mapfield(fieldtype, cfg, logger)
        if fieldtype is False:
            logger.error('Cannot map field.  Cannot load schema')
            return False

        fieldtype, fieldformat = mapformat(fieldtype, fieldformat, fieldwidth, cfg, logger)
        if isinstance(fieldformat, bool):
            if fieldformat is False:
                logger.error('Cannot map format.  Cannot load schema')
                return False

        # add to query
        qry = qry + fieldname + ' ' + fieldtype + ' ' + fieldformat + nullable + ','

    # when system_table add is_customer_owned field
    if table_upper in is_system_table:
        qry = qry + is_customer_owned + ','

    # remove last comma
    qry = qry[:-1] + ')'

    logger.info(qry)

    cur = run_msql(qry, conn, cfg, logger)
    if isinstance(cur, bool):
        if cur is False:
            return False

    return True


def loadSequence(cfg, logger, conn):

    qrylst = []

    try:
        oedbname = cfg['oedbname']
        fwd_sequence = cfg['fwd_sequence']
        fn = cfg['stage'] + '/%s.sequences' % oedbname
    except Exception as e:
        logger.error(e)
        return False

    logger.info('Load Sequences for %s')

    # read structure from disk
    try:
        f = open(fn, 'r')
        content = f.readlines()
    except Exception as e:
        logger.error(e)
        return False
    f.close()

    for line in content:
        tokens = line.split(',')
        seqnum = tokens[0]
        seqname = tokens[1]
        curval = tokens[2]
        seqmin = tokens[3]
        # read but ignore the maxvalue 
        seqmax = tokens[4]

        seqname = seqname.replace('#FWD_SEQUENCE#', fwd_sequence)

        qry = 'DROP SEQUENCE IF EXISTS %s' % seqname
        qrylst.append(qry)
        qry = 'CREATE SEQUENCE %s INCREMENT BY 1 MINVALUE %s NOMAXVALUE START WITH %s CYCLE' % (
            seqname, seqmin, curval)
        qrylst.append(qry)

    for qry in qrylst:
        cur = run_msql(qry, conn, cfg, logger)
        if isinstance(cur, bool):
            if cur is False:
                return False

    conn.commit()
    cur.close()

    return True


def mapfield(source, cfg, logger):

    try:
        target = cfg['mappings'][source]
        return target
    except KeyError as e:
        logger.error('Mapfield key missing %s' % source)
        logger.error(e)
    return False


def mapformat(fieldtype, fieldformat, fieldwidth, cfg, logger):

    logger.info('Format multiplier %s' % cfg['format_multiplier'])

    if fieldtype == 'varchar':
        try:
            if int(fieldwidth) >= int(cfg['text_to_varchar_cutoff']):
                fieldtype = 'text'
            if fieldwidth == '':
                if '(' in fieldformat:
                    fieldformat = fieldformat.split('(')[1].split(')')[0]
                    # fieldformat = '(' + str(int(fieldformat.split('(')[0]) * int(cfg['format_multiplier'])) + ')'
                    fieldformat = '(' + str(int(int(fieldformat.split('(')[0]) * float(cfg['format_multiplier']))) + ')'
                else:
                    fieldformat = '(' + str(cfg['format_default']) + ')'
            else:
                fieldformat = '(' + fieldwidth + ')'
        except Exception as e:
            logger.error('Cannot determine field format for %s - %s' %
                         (fieldtype, e))
            return False
    else:
        fieldformat = ''

    return fieldtype, fieldformat


def postprocessData(mdbname, table, cfg, conn, logger):
    '''
    for each TABLENAME_*.clob in the stage directory :
       fieldname is fn.split('_')[1]
       for each line in fn :
          for each field that ends in .clob
             read the file associated with that field
             find the record in the database where fieldname = file
             update that record and set the fieldname to the file contents
    '''
    logger.info('Post Processing Table %s.%s' % (mdbname, table))

    qrylist = []

    try:
        stage = cfg['stage']
        globstring = stage + '/' + table + '_*.clob'
    except Exception as e:
        logger.error(e)
        return False

    files = glob.glob(globstring)
    for file in files:
        logger.info('Processing file %s' % file)

        try:
            # fieldname = file.split('_')[1]
            fieldname = file.split('/')[1].split('_')[1]
            with open(file, 'r') as f:
                clob = f.read()
            clob = clob.replace("'", '"')
            # escape single quotes
            qry = "UPDATE %s.%s SET %s = '%s' WHERE %s = '%s'" % (
                mdbname, table, fieldname, clob, fieldname, file)
            qrylist.append(qry)
        except Exception as e:
            logger.error(e)
            return False

    logger.info(qrylist)
    for qry in qrylist:
        cur = run_msql(qry, conn, cfg, logger)
        if cur == False:
            return False

        conn.commit()
        cur.close()

    return True


def postprocessSchema(table, cfg, logger):
    '''
    read back each line, if split(';')[4] > 0 then do not add the line
    instead replace [1] with [1] + an increasing number from 1 until = [4] and add that
    except for [0] in extent_special then just csv values as rows from qextent_[special]

    datetime-tz will be converted into timestamp <field> and integer
    <field_offset>
    '''

    logger.info('Postprocessing Schema for %s' % table)

    extent_special_dict = {}
    reserved_words_dict = {}
    try:
        stage = cfg['stage']
        extent_special = cfg['extent_special']
        datetime_index_suffix = cfg['datetime_index_suffix']
        reserved_words = cfg['reserved_words']
        reserved_suffix = cfg['reserved_suffix']

        for line in extent_special.split(','):
            extent_special_dict[line] = 1

        for line in reserved_words.split(','):
            reserved_words_dict[line] = 1

        fn = stage + '/' + table + '.dat'
        with open(fn, 'r') as f:
            schema = f.readlines()
        f.close()
    except Exception as e:
        logger.error(e)
        return False

    newschema = []
    foundChanges = False
    for line in schema:
        tokens = line.split(';')

        # handle special cases
        if tokens[1] in extent_special_dict:
            try:
                foundChanges = True
                lookup = 'extent_' + tokens[1]
                extent_special_fields = cfg[lookup]
                special_tokens = extent_special_fields.split(',')
                for t in special_tokens:
                    newline = tokens[0] + ';' + t + ';' + tokens[2] + ';' + tokens[3] + ';0;' + tokens[5] + ';' + tokens[6] + ';' + tokens[7]
                    newschema.append(newline)
            except KeyError as e:
                logger.error('Error handling special extent field %s - %s' %
                             (tokens[1], e))
                return False

        elif int(tokens[4]) > 0:
            # handle extents
            foundChanges = True

            c = 1
            while c <= int(tokens[4]):
                newline = tokens[0] + ';' + tokens[1] + reserved_suffix + str(c) + ';' + tokens[2] + ';' + tokens[3] + ';0;' + tokens[5] + ';' + tokens[6] + ';' + tokens[7]
                newschema.append(newline)
                c = c + 1
        else:

            # if field is not in reserved words add the suffix
            try:
                uppertoken = str.upper(tokens[1])
                t = reserved_words_dict[uppertoken]

                newline = tokens[0] + ';' + tokens[1] + reserved_suffix + ';' + tokens[2] + ';' + tokens[3] + ';0;' + tokens[5] + ';' + tokens[6] + ';' + tokens[7]
                newschema.append(newline)
                foundChanges = True
            except Exception:
                newschema.append(line)
                # pass

            # handles timestamp and datetime
            if tokens[2] == 'datetime-tz':
                foundChanges = True
                # newline = tokens[0]  + ';' + tokens[1] + datetime_index_suffix + ';' + tokens[2] + ';' + tokens[3] + ';0;'+ tokens[5] + ';' + tokens[6] + ';' + tokens[7]
                # Maybe the default format must be changed for datetime-tz
                '''
                if tokens[5] == '?':
                    tokens[5] = ''
                newline = tokens[0] + ';' + tokens[1] + ';' + tokens[2] + ';' + '99/99/999' \
                + ';' + tokens[4] + ';' + tokens[5] + ';' + tokens[6] + ';' + tokens[7]
                newschema.append(newline)
                '''
                newline = tokens[0] + ';' + tokens[1] + datetime_index_suffix + \
                ';' + 'integer' + ';' + '>>>>>>>9' + ';0;' + '0' + ';' + tokens[6] + ';' + '11\n'
                newschema.append(newline)
            # else:
                # newschema.append(line)

    if not foundChanges:
        return True

    try:
        logger.info('Rewriting %s' % fn)
        logger.info(newschema)
        with open(fn, 'w') as f:
            f.writelines(newschema)
        f.close()
    except Exception as e:
        logger.error(e)
        return False

    return True


def readdotp(dotp, cfg, logger):
    '''
    reads .p source from file into a string
    looks in current directory unless fully qualified in the YAML file
    '''

    if os.path.isfile(dotp) and os.access(dotp, os.R_OK):
        try:
            with open(dotp, 'r') as f:
                query = f.read()
        except Exception as e:
            logger.error(e)
            return False

    else:
        logger.error('Cannot find or read file %s' % dotp)
        return False

    return query


def runabl(query, cfg, logger):
    '''
    Run an ABL function inline
    '''

    try:
        dlc = cfg['dlc']
        oedbpath = cfg['oedbpath']
        oedbname = cfg['oedbname']
        oedbuser = cfg['oedbuser']
        oedbpassword = cfg['oedbpassword']
        pfparams = cfg['pfparams']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    result = setoedlc(cfg, logger)
    if result is False:
        logger.error('Exiting')
        return False

    logger.debug('Running query >%s>' % query)

    try:
        tf = tempfile.NamedTemporaryFile()

        with open(tf.name, "w") as t:
            t.write(query)

        if not oedbuser == 'None' and not oedbpassword == 'None':
            userstring = '-U %s -P %s' % (oedbuser, oedbpassword)
        else:
            userstring = ''

        runstring = 'TERM=ansi;export $TERM;_progres -db %s/%s %s' % (
            oedbpath, oedbname, userstring)
        runstring = runstring + ' -p ' + tf.name + ' ' + pfparams
        logger.debug(runstring)

        oecmd = Popen(runstring,
                      shell=True,
                      stdout=PIPE,
                      stderr=PIPE)
        x = oecmd.communicate()[0].splitlines()
        oecmd.wait()

        t.close()

        foundErrors = False
        # check for errors
        for line in x:
            line = line.decode('utf-8')
            logger.debug(line)
            if '**' in line:
                logger.error(line)
                foundErrors = True

            # only need to check first line
            else:
                break

        if foundErrors:
            return False

        return x
    except Exception as e:
        logger.error('ERROR ABL exception')
        logger.error(e)
        return False


def run_msql(qry, conn, cfg, logger):

    logger.info('running %s' % qry)

    try:
        stop_on_duplicate = cfg['stop_on_duplicate']
        stop_on_error = cfg['stop_on_error']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    cur = conn.cursor()
    try:
        x = cur.execute(qry)

    except mariadb.IntegrityError as e:
        logger.error('Error inserting %s ' % qry)
        logger.error(e)
        if stop_on_duplicate is True:
            logger.error('Stop on Duplicate.  Exiting')
            conn.rollback()

            return False
        else:
            logger.error('Ignoring Duplicate %s ' % qry)
            conn.rollback()
    except mariadb.Warning as e1:
        logger.error('Warning %s' % qry)
        logger.error('Data may be truncated or incorrect on row')
        logger.error(e1)
        if stop_on_error is True:
            logger.error('stopOnError is True so exiting')
            conn.rollback()
            return False

    except mariadb.DataError as e2:
        logger.error('DataError %s' % qry)
        logger.error(e2)
        if stop_on_error is True:
            logger.error('stopOnError is True so exiting')
            conn.rollback()
            return False
    except Exception as e3:
        logger.error('General Exception Error %s' % qry)
        logger.error(e3)
        if stop_on_error is True:
            logger.error('stopOnError is True so exiting')
            conn.rollback()
            return False

    return cur


def run_oesql(conn, curs, qry, logger):

    try:
        curs.execute(qry)
        result = curs.fetchall()
    except Exception as e:
        logger.error('ERROR running query %s' % qry)
        logger.error(e)
        return (curs, False)

    if type(result) is str:
        logger.error('ERROR running query %s ( string returned, not cursor )' % qry)
        return (curs, False)

    return (curs, result)


def run_oesql_update(conn, curs, qry, logger):
    try:
        curs.execute(qry)
    except Exception as e:
        logger.error(f'ERROR running query %s {e}' % qry)
        return (curs, False)

    try:
        conn.commit()
    except Exception as e:
        logger.error(f'Error committing query %s {e}' % qry)
        return (curs, False)

    return (curs, True)


def setoedlc(cfg, logger):
    '''
    Sets DLC
    '''

    logger.debug('Setting up ABL environment ( DLC) ')
    try:
        dlc = cfg['dlc']
    except KeyError as e:
        logger.error(f'YAML file is missing key {e}')
        return False

    os.environ['DLC'] = dlc
    dlcpath = os.environ['PATH']
    if dlc not in dlcpath:
        dlcpath = dlc + "/bin:" + dlc + "/perl/bin:" + dlcpath
        os.environ['PATH'] = dlcpath
    return True


def tableExists(table, mdbname, cfg, conn, logger):

    qry = "select case when (select count(*) from INFORMATION_SCHEMA.TABLES where TABLE_NAME='%s' and TABLE_SCHEMA = '%s') = 1 then True else False end" % (table, mdbname)
    cur = run_msql(qry, conn, cfg, logger)
    result = cur.fetchone()
    cur.close()

    if result[0] == True:
        return True
    return False


def tablewrapper(cfg, logger):
    '''
    get list of tables from the Openedge Schema
    '''

    logger.info('Extracting Table List')
    tablelist = []

    try:
        abltables = cfg['abltables']
        query = readdotp(abltables, cfg, logger)
        exclude_tables = cfg['exclude_tables']

        tables = runabl(query, cfg, logger)
        if tables is False:
            logger.error('Cannot continue, tables cannot be extracted.  Exiting')
            return False

        for line in tables:

            tablename = byteify(line.decode())

            if tablename in exclude_tables:
                logger.info('Table %s in exclude list, skipping' % tablename)
                continue
            if 'CDC_' in tablename:
                logger.debug('Skipping CDC table %s' % tablename)
                continue
            tablelist.append(tablename)

    except Exception as e:
        logger.error('Error extracting tables')
        logger.error(e)
        return False

    return tablelist
