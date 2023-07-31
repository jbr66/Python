#!/usr/bin/python3
'''
  NAME
    simple.py	-	Simple Python procedure

  AUTHOR
    Written by John Brink

  REVISION HISTORY
  -------------------------------------------------------
    1.0 07/28/2021 jbr - Display 'Hello World'
    1.1	07/30/2021 j6b - Play with output
  -------------------------------------------------------
'''

import os
import sys
import argparse

t       = ('Hello', 'World', 'Britt & Joris', 'Lonneke', 'Nicole Le Haen')
ln      = 1
header  = ['Nr', 'Omschrijving', 'Balans']

print('Hello World')
print("%-2s %-20s %6s"%(header[0],header[1],header[2]))
print(40*'-')

for i in t * 3:
	print("%2d %-20s %6s"%(ln,i,(ln%2 == 0)))
	ln += 1
