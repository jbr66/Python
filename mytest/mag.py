#!/usr/bin/python3
'''
NAME
    mag.py    - Read JSON file mag.txt and process grades

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
        return round(float(totalSum / totalFactor), 2)


file = 'mag.txt'

try:
    with open(file, 'r') as f:
        data = json.load(f)

except Exception as e:
    print("Error reading %s - %s" % (file, e))
    sys.exit(1)

for s in data.keys():
    print('Student: %s' % s.capitalize())
    line = '+' + 29 * '-' + '+'
    print(line)
    header = '| %11s | %4s | %5s |' % ('vak'.center(11), 'grade', 'round')
    print(header)
    print(line)
    somMean = 0
    for v in data[s].keys():
        mean = calculateMean(data[s][v])
        somMean += mean
        print('| %11s | %5.2f | %3.0f   |' % (v, mean, round(mean, 0)))

    print(line)
    print('| %11s | %5.2f | %3.0f   |' % ('Mean'.center(11),
                                          somMean / len(data[s].keys()),
                                          round(somMean / len(data[s].keys()), 0)))
    print(line)
    print()
