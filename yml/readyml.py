#!/usr/bin/env python3
'''
NAME
	readyml.py - Read yaml file

AUTHOR
	Written by John Brink

REVISION HISTORY
-------------------------------------------------------
	1.0	12/01/2023 john - Initial version
-------------------------------------------------------
vim:ts=4
'''

import yaml
import json

with open('example.yml', 'r') as file:
	ex = yaml.safe_load(file)

print(ex)
print(42*'-')
print("Output as JSON")
print(json.dumps(ex, indent=2))
print(42*'-')

