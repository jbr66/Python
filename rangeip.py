#!/usr/bin/python

import ipaddress as ip
import argparse
import sys

parser = argparse.ArgumentParser(description='Provide IP-address for range of IP-addresses',
               epilog='Created by JBR')
parser.add_argument('IPaddress', metavar='IPADDRESS', type=str)
args = parser.parse_args()

try:
  ip2check = ip.ip_address(args.IPaddress)
except ValueError:
  print("Invalid ipaddress provided")
  sys.exit(1)
except:
  print("Something else is wrong")
  sys.exit(2)

max = 32

i = max
while (i > 16):
   n = ip.ip_network(ip2check.exploded + '/' + str(i), strict = False)
   print("Range for", n, ":", n[0], "-", n[-1], '(', str(len(list(n.hosts()))), ')', str(n.num_addresses))
   i -= 1

sys.exit(0)
