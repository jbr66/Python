#!/usr/bin/python

import ipaddress as p

Myip = p.ip_address('192.168.1.5')
Mynet = p.ip_network('192.168.1.0/24')
Myinterface = p.ip_interface('192.168.1.5/24')

print("IP address: " + Myip.exploded)
print("Netmask of network: " + str(Myinterface.netmask))
print(Myip in Mynet.hosts())
