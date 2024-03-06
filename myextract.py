#!/usr/bin/python3
'''
NAME
	myextract.py	- Extract a file and generate dummy files for m3u list
'''

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('file', help="provide file that needs to be 'extracted'")

args = parser.parse_args()
file = args.file

try:
	with open(file,'r') as f:
		lines = f.readlines()

except Exception as e:
	print('Unable to read %s - %s' % (file, e))
	sys.exit(1)

for line in lines:
	line = line.strip()
	tokens = line.split('/')

print(tokens)
