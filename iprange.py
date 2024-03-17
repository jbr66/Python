#!/usr/bin/python3
'''
NAME
    iprange.py - Provides possible IP-address based on range

AUTHOR
    Written by John Brink

REVISION HISTORY
-------------------------------------------------------------
    1.0 08/09/2023 jbr - initial version
-------------------------------------------------------------
'''

from ipaddress import ip_address
import argparse


# Define functions
def ips(start, end):
    '''Return IPs in IPv4 range, inclusive.'''
    start_int = int(ip_address(start).packed.hex(), 16)
    end_int = int(ip_address(end).packed.hex(), 16)
    return [ip_address(ip).exploded for ip in range(start_int, end_int)]


# Define parameters

parser = argparse.ArgumentParser(
    description="generate list of IP-addresses")
parser.add_argument('start',
                    help="provide start address")
parser.add_argument('end',
                    help="provide end address")
parser.add_argument('-d', '--debug',
                    help="display debug information",
                    action="store_true")
parser.add_argument('-v', '--verbosity', action="count", default=0,
                    help="increase output verbosity")
args = parser.parse_args()

# Setting variables
start = args.start
end = args.end
debug = args.debug
verbose = args.verbosity

if debug:
    print(42 * '-')
    print(args)
    print(42 * '-')

print(ips(start, end))
