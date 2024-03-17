#!/usr/bin/python3

import sys
import argparse

print('hallo')
parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('tofile')

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
    with open(tofile, 'w') as f:
        f.write(data)
except Exception as e:
    print('Error writing data to %s - %s' % (tofile, e))
    sys.exit(1)
