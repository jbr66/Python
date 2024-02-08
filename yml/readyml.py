#!/usr/bin/env python3
'''
NAME
	readyml.py - Read yaml file

AUTHOR
	Written by John Brink

REVISION HISTORY
-------------------------------------------------------
	1.0	12/01/2023 john - Initial version
        1.1     12/09/2023 john - Using input parameters
	1.2	02/08/2024 john - Example for config
-------------------------------------------------------
vim:ts=4
'''

import os, sys
import yaml
import json
import argparse

# Define parameters

parser = argparse.ArgumentParser(
        description="Process given yaml file"
        )
parser.add_argument('file',
        help="provide yaml based file"
        )
args = parser.parse_args()

file2read = args.file

if not os.path.isfile(file2read):
    print("File {} could not be found - Exiting".format(file2read))
    sys.exit(1)

try:
    with open(file2read, 'r') as file:
        ex = yaml.safe_load(file)
except PermissionError:
    print("Not enough permissions to open file {}".format(file2read))
    sys.exit(2)
except e:
    print("Failed to open file {}".format(file2read))
    sys.exit(3)

print(ex)
print(42*'-')
print("Output as JSON")
print(json.dumps(ex, indent=2))
print(42*'-')

print('Example of config:')
for i in ex:
	print('{} : {}'.format(i,ex[i]))

print('Mapping: {}'.format(ex['mappings']['character']))
