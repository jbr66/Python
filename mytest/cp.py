#!/usr/bin/python3

import sys
import argparse
import getpass

try:
    name = getpass.getuser()
except Exception as e:
    print("Error getting username - %s" % e)
    sys.exit(2)

print('hallo %s' % getpass.getuser())
parser = argparse.ArgumentParser()
parser.add_argument('file',
                    help='Name of file to copy from')
parser.add_argument('tofile',
                    help='Name of file to copy to, but will NOT overwrite file')

args = parser.parse_args()
file = args.file
tofile = args.tofile

try:
    with open(file, 'r') as f:
        data = f.read()
except FileNotFoundError:
    print("File %s couldn't be found" % file)
    sys.exit(2)
except Exception as e:
    print('Error reading %s - %s' % (file, e))
    sys.exit(1)

# create new file
try:
    with open(tofile, 'x') as f:
        f.write(data)
except Exception as e:
    print('Error writing data to %s - %s' % (tofile, e))
    sys.exit(1)
