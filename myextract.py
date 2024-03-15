#!/usr/bin/python3
'''
NAME
    myextract.py    - Extract a file and generate dummy files for m3u list
'''

import argparse
import sys
import subprocess

parser = argparse.ArgumentParser(prog='myextract.py', description='Generate some dummy files for m3u list', epilog='2024 - JeBe-IT')
parser.add_argument('file', help="provide file that needs to be 'extracted'")
parser.add_argument('-d', dest='subdir', default='data', help="provide directory for storing files")

args = parser.parse_args()
file = args.file
subdir = args.subdir

try:
    with open(file,'r') as f:
        lines = f.readlines()

except Exception as e:
    print('Unable to read %s - %s' % (file, e))
    sys.exit(1)

'''
    format line: <dir>/<Artist> - <Album>/<track>
'''
tokens = []
music = {}
for line in lines:
    line = line.strip()
    tokens = line.split('/')
    artist = tokens[1].split('-')[0].strip()
    cd = tokens[1].split('-')[1].strip()
    song = tokens[2].strip()
    if not artist in music:
        music[artist] = {}
        music[artist][cd] = []
        music[artist][cd].append(song)
    elif not cd in music[artist]:
        music[artist][cd] = []
        music[artist][cd].append(song)
    else:
        music[artist][cd].append(song)

# Generate files
for artist in music.keys():
    for cd in music[artist].keys():
        try:
            if "'" in artist or "'" in cd:
                cmd = 'mkdir -p %s/"%s"/"%s"' % (subdir,artist,cd)
            else:
                cmd = "mkdir -p %s/'%s'/'%s'" % (subdir,artist,cd)
            subprocess.run(cmd, shell=True)
        except Exception as e:
            pass

        for song in music[artist][cd]:
            try:
                if not "'" in song:
                    cmd = "touch %s/'%s'/'%s'/'%s'" % (subdir,artist,cd,song)
                else:
                    cmd = 'touch %s/"%s"/"%s"/"%s"' % (subdir,artist,cd,song)
                subprocess.run(cmd, shell=True)
            except Exception as e:
                print('Failed to generate file %s' % e)
                sys.exit(1)
