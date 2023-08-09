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

def ips(start, end):
    '''Return IPs in IPv4 range, inclusive.'''
    start_int = int(ip_address(start).packed.hex(), 16)
    end_int = int(ip_address(end).packed.hex(), 16)
    return [ip_address(ip).exploded for ip in range(start_int, end_int)]


print(ips('192.168.1.240', '192.168.2.5'))
