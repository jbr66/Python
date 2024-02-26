#!/usr/bin/python3
'''
NAME
	mag.py	- Read JSON file mag.txt and process grades

'''

import json
import sys

def calculateMean(a):
	'''
	calculateMean needs array with (grade,factor) pairs
	it will return the mean of the grades
	'''

	i = 0
	totalSum = 0
	totalFactor = 0
	if len(a) == 0:
		return 0
	while i < len(a):
		totalSum += a[i][0] * a[i][1]
		totalFactor += a[i][1]
		i += 1

	if totalFactor == 0:
		return 0
	else:
		return(round(float(totalSum/totalFactor),2))


file = 'mag.txt'

try:
	with open(file,'r') as f:
		data = json.load(f)

except Exception as e:
	print("Error reading %s - %s" % (file,e))
	sys.exit(1)

line = '+' + 28*'-' + '+'
print(line)
header = '| %-10s | %4s | %5s |' % ('vak','grade','round')
print(header)
print(line) 
for v in data.keys():
	mean = calculateMean(data[v])
	print('| %10s | %5.2f | %3.0f   |' % (v,mean,round(mean,0)))

print(line)
