#!/usr/bin/python3
'''
  NAME
    m3u.py	- Create m3u playlist of songs for given directory

  AUTHOR
    Written by John Brink

  REVISION HISTORY
  ----------------------------------------------------------------
    1.0 07/31/2023 jbr - Initial version
  ----------------------------------------------------------------
'''

import os
import sys
import argparse

def get_files(path):
  r = []
  for file in os.listdir(path):
    if os.path.isfile(os.path.join(path, file)):
      r.append(os.path.join(path, file))
  
  if len(r) > 0:
    return(r)
  else:
    return(0)

parser = argparse.ArgumentParser(
               description="Generate playlist for given directory")
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
  if verbose >= 2:
    print("Found the following files:")
    print(80*"-")
    for f in files:
      print(f)
    print(80*"-")
else:
  print(f"{dir} doesn't contain any files")
  sys.exit(0)
