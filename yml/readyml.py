#!/usr/bin/env python3
'''
NAME
    readyml.py - Read yaml file

AUTHOR
    Written by John Brink

REVISION HISTORY
-------------------------------------------------------
    1.0 12/01/2023 john - Initial version
    1.1 12/09/2023 john - Using input parameters
    1.2 02/08/2024 john - Example for config
    1.3 03/20/2024 john - Process configfile
-------------------------------------------------------
vim:ts=4
'''

import os
import sys
import yaml
import json
import argparse

list_of_bool = ['--etl',]
str_to_bool = ['True','False']

def createConfig(cfg):
    '''
    Returns an dictionary with all settings
    from the file
    '''

    config = {}
    for i in cfg:
        config[i] = cfg[i]

    return cfg


# Define parameters

parser = argparse.ArgumentParser(
    description="Process given yaml file")
parser.add_argument('file',
                    help="provide yaml based file")
parser.add_argument('--etl')

args = parser.parse_args()

file2read = args.file
for a in sys.argv:
    print(a)
    if a in list_of_bool:
        print('a is %s' % a[2:])

if args.etl.capitalize() in str_to_bool:
    cetl = eval(args.etl)
else:
    print('Only False or True can be used for --etl')
    sys.exit(1)

print('cetl: %s' % cetl)
if not os.path.isfile(file2read):
    print("File {} could not be found - Exiting".format(file2read))
    sys.exit(1)

try:
    with open(file2read, 'r') as file:
        ex = yaml.safe_load(file)
except PermissionError:
    print("Not enough permissions to open file {}".format(file2read))
    sys.exit(2)
except Exception as e:
    print("Failed to open file {} - {}".format(file2read, e))
    sys.exit(3)

'''
print(ex)
print(42 * '-')
print("Output as JSON")
print(json.dumps(ex, indent=2))
print(42 * '-')

print('Example of config:')
for i in ex:
    print('{} : {}'.format(i, ex[i]))

print('Mapping: {}'.format(ex['mappings']['character']))
'''

cfg = createConfig(ex)
print('Change default value to parameter value')
cfg['etl'] = cetl

print("type of ex['etl']: %s" % type(ex['etl']))
print("type of cfg['etl']: %s" % type(cfg['etl']))
print("type of cetl: %s" % type(cetl))

if cfg['etl']:
    print('Simple test 1 no operator')
if cfg['etl'] is True:
    print('Simple test 2 operator is "is"')
if cfg['etl'] == True:
    print('Simple test 3 operator is "=="')
