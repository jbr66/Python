#!/usr/bin/python3
'''
NAME
	readdir	-	Read directory

Output of ls -1
	'1 - Title 1.flac'
	'10 - Title 10.flac'
	'13 - Title 13.flac'
	'2 - Title 2.flac'
	'20 - Title 20.flac'
	'3 - Title 3.flac'
	'30 - Title 30.flac'
	'32 - Title 32.flac'
	'34 - Title 34.flac'
	'4 - Title 4.flac'
	'5 - Title 5.flac'
	'54 - Title 54.flac'
	'6 - Title 6.flac'
	'65 - Title 65.flac'
	'7 - Title 7.flac'
	'8 - Title 8.flac'
	'87 - Title 87.flac'
	'9 - Title 9.flac'
	'90 - Title 90.flac'

Result of readdir.py:
	  1 - Title 1.flac
	  2 - Title 2.flac
	  3 - Title 3.flac
	  4 - Title 4.flac
	  5 - Title 5.flac
	  6 - Title 6.flac
	  7 - Title 7.flac
	  8 - Title 8.flac
	  9 - Title 9.flac
	 10 - Title 10.flac
	 13 - Title 13.flac
	 20 - Title 20.flac
	 30 - Title 30.flac
	 32 - Title 32.flac
	 34 - Title 34.flac
	 54 - Title 54.flac
	 65 - Title 65.flac
	 87 - Title 87.flac
	 90 - Title 90.flac


'''

import glob
import argparse
import os
import sys

parser = argparse.ArgumentParser(
    epilog='2024 - JeBe-IT')
parser.add_argument('directory', nargs='?', default='.',
    help='Supply directory to be read - default: current')
parser.add_argument('-R', '--recursive', dest='indepth', action='store_true',
    help='Supply directory to be read - default: current')

args = parser.parse_args()
print(args)
dir = args.directory
indepth = args.indepth
if not os.path.isdir(dir):
    print("%s isn't a directory - Exiting" % dir)
    sys.exit(1)

pattern = '*.flac'
dir = dir + '/' + pattern

f_dir = {}
files = glob.glob(dir, recursive=indepth)
for f in files:
    file = f.split('/')[-1]
    file_strip = file.split('-')
    f_dir[int(file_strip[0].strip())] = file_strip[1].strip()

sort_nr = sorted(f_dir.keys())
for i in sort_nr:
    print('%3d - %s' % (i,f_dir[i]))
