#!/usr/bin/python3
'''
  NAME
    m3u.py	- Create m3u playlist of songs for given directory

  AUTHOR
    Written by John Brink

  REVISION HISTORY
  ----------------------------------------------------------------
    1.0 07/31/2023 jbr - Initial version
    1.1 08/06/2023 j6b - Get directory sorted
  ----------------------------------------------------------------
'''

import os
import sys
import argparse
import subprocess

'''
# v1.0
def get_files(path):
  r = []
  for file in os.listdir(path):
    if os.path.isfile(os.path.join(path, file)):
      r.append(os.path.join(path, file))
  
  if len(r) > 0:
    return(r)
  else:
    return(0)
'''

# v1.1
def get_files(path):
  cmd = '/bin/ls'

  r = subprocess.run([cmd, path], capture_output=True, text=True)

  if len(r.stdout) > 0:
    return(r.stdout.split('\n'))
  else:
    return(0)

'''
  Example:

	#EXTM3U
	#EXTINF:233,Vonda Shepard - Searchin' My Soul
	01 - Searchin' My Soul.flac
	#EXTINF:163,Vonda Shepard - Ask The Lonely
	02 - Ask The Lonely.flac
	#EXTINF:188,Vonda Shepard - Walk Away Renee
	03 - Walk Away Renee.flac
	#EXTINF:232,Vonda Shepard - Maryland
	14 - Maryland.flac
'''
def create_m3u(path, files):
  print('#EXTM3U')
  for f in files:
    if ('.mp3' in f) or ('.flac' in f):
      print('#EXTINF:{}'.format(f))
      print('{}/{}'.format(path,f))


parser = argparse.ArgumentParser(
        description="Generate playlist for given directory",
        epilog='2024 - JeBe-IT')
parser.add_argument('directory',
               help="provide directory with songs to generate \
                     playlist for")
parser.add_argument('-d', '--debug',
               help="display debug information",
               action="store_true")
parser.add_argument('-v', '--verbosity', action="count", default=0,
               help="increase output verbosity")
args = parser.parse_args()

# Setting variables
dir     = args.directory
debug   = args.debug
verbose = args.verbosity
files   = []

if debug:
  print(42*'-')
  print(f"Provided parameters for '{__file__}'")
  #print("Provided parameters for '{}'".format(__file__))
  print("%-10s: %30s"%('dir',dir))
  print("%-10s: %30s"%('debug',debug))
  print("%-10s: %30d"%('verbose',verbose))
  print(42*'-')

if verbose >= 2:
  print(f"Running '{__file__}'")

if not os.path.isdir(dir):
  print(f"{dir} is not a directory - exiting....")
  sys.exit(1)
else:
  # Read files from directory
  files = get_files(dir)

if not files == 0:
  if debug:
    print(files)
  if verbose >= 2:
    print("Found the following files:")
    print(80*"-")
    for f in files:
      print(f)
    print(80*"-")
  create_m3u(dir, files)
else:
  print(f"{dir} doesn't contain any files")
  sys.exit(0)
