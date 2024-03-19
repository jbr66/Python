#!/usr/bin/env python3

import sys
import os
# import yaml
import argparse
import socket
import tempfile
from subprocess import Popen, PIPE
# import time

hostname = socket.gethostname()

# default
level = 'Medium'


parser = argparse.ArgumentParser(description='Enable CDC')
parser.add_argument("--db", help="/path/to/db")
parser.add_argument("--ldb", help="db logical name, eg.  qaddb")
parser.add_argument("--oe", help="/path/to/openedge")
parser.add_argument("--p", help="query template")
parser.add_argument("--t", help="tmp directory")
parser.add_argument("--dataarea", help="data area")
parser.add_argument("--indexarea", help="index area")
parser.add_argument("--level", help="level = medium or maximum")
parser.add_argument("--owner", help="schema owner, eg.PUB")


try:
    args = parser.parse_args()
    dlcdir = args.oe
except SystemExit:
    print(__doc__)
    sys.exit(2)


def runabl(thisquery, db, ldb, oe):
    # print('Running ABL Query>> %s' % thisquery)

    try:
        tf = tempfile.NamedTemporaryFile()

        with open(tf.name, "w") as t:
            t.writelines(thisquery)

        runstring = 'TERM=ansi;export $TERM;_progres -db ' + db
        runstring = runstring + ' -ld ' + ldb + ' -p ' + tf.name \
            + ' -cpinternal utf-8 -cpstream utf-8 -NL -yr4def ' \
            + '-d ymd -ServerType 4gl -cpcoll ICU-UCA -b '
        print(runstring)

        oecmd = Popen(runstring, shell=True, stdout=PIPE, stderr=PIPE)
        x = oecmd.communicate()[0].splitlines()
        oecmd.wait()
        try:
            t.close()
        except Exception as e:
            print('Closing failed - %s' % e)
            pass

        return x
    except Exception as e:
        print('ERROR ABL exception - %s' % e)
        return False


def setoe(oe):
    print('Setting up ABL environment')
    os.environ['DLC'] = oe
    dlcpath = os.environ['PATH']
    if 'dlc' not in dlcpath:
        dlcpath = dlcdir + "/bin:" + oe + "/perl/bin:" + dlcpath
        os.environ['PATH'] = dlcpath
    return


def readquerytemplate(p):
    try:
        f = open(p)
    except Exception as e:
        print('Could not open file, please check --p for '
              + 'template existence and permissions - %s' % e)
        sys.exit(2)

    lines = f.readlines()
    return lines


def replacemacros(lines, ldb, t, dataarea, indexarea, level, owner):
    code = []
    for line in lines:
        if '#TMPDIR#' in line:
            line = line.replace('#TMPDIR#', t)

        if '#SERVICENAME#' in line:
            line = line.replace('#SERVICENAME#', ldb)

        if '#DATA#' in line:
            line = line.replace('#DATA#', dataarea)

        if '#INDEX#' in line:
            line = line.replace('#INDEX#', indexarea)

        if '#LEVEL#' in line:
            line = line.replace('#LEVEL#', level)

        if '#OWNER#' in line:
            line = line.replace('#OWNER#', owner)

        code.append(line)

    # print(code)
    return code


########################
# MAIN
########################

if __name__ == '__main__':
    lines = readquerytemplate(args.p)

    if args.t:
        if not os.path.exists(args.t):
            print('--t path does not exist')
            print(__doc__)
            sys.exit(2)
    else:
        print('you must supply -t tmp directory path ')
        print(__doc__)
        sys.exit(2)

    if args.oe:
        setoe(args.oe)
    else:
        print('please supply --oe openedgedirectory')
        print(__doc__)
        sys.exit(2)

    if not args.ldb:

        print('please supply a logical databse name --ldb')
        print(__doc__)
        sys.exit(2)

    if not args.dataarea:

        print('please supply a data area for the CDC storage area --dataarea')
        print(__doc__)
        sys.exit(2)

    if not args.indexarea:

        print('please supply an index area for the CDC storage area --indexarea')
        print(__doc__)
        sys.exit(2)

    if not args.owner:

        print('Owner not supplied, using PUB')
        owner = 'PUB'
    else:
        owner = args.owner

    if args.level:
        if args.level == 'Medium' or args.level == 'Maximum':
            level = args.level
        else:
            print('--level must be 2 or 3')
            print(__doc__)
            sys.exit(2)

    code = replacemacros(
        lines,
        args.ldb,
        args.t,
        args.dataarea,
        args.indexarea,
        level,
        owner)

    if args.oe:
        setoe(args.oe)
    else:
        print('please supply --oe openedgedirectory')
        print(__doc__)
        sys.exit(2)

    if not args.db:
        print('please supply --db /path/to/database.db')
        print(__doc__)
        sys.exit(2)
    else:
        if not os.path.isfile(args.db):
            print('cannot file database %s with --db' % args.db)
            print(__doc__)
            sys.exit(2)

    # now run the .p generation file
    result = runabl(code, args.db, args.ldb, args.oe)
    if not result:
        print('Could not run ABL code %s' % code)
        sys.exit(2)

    count = 0

    # run policies
    for line in result:
        count = count + 1
        line = line.decode('utf-8')
        print('Running CDC policy %s' % line)
        code = readquerytemplate(line)
        result = runabl(code, args.db, args.ldb, args.oe)
        if result is False:
            print('Could not run CDC policy code %s SKIPPING' % code)
            print(result)
        else:
            print(result)

print('** Done **')
sys.exit(0)
