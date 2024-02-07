#!/usr/bin/python

import argparse

parser = argparse.ArgumentParser(prog='parser_example',
                    description='Process some integers.', 
                    epilog='Created by JBR')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
parser.add_argument('--min', dest='accumulate', action='store_const',
                    const=min, default=max,
                    help='find the min (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))
