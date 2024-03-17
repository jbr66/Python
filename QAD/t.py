#!/usr/bin/env python3
'''
Problems with TGW

Run the following command to get all requirements
    $ pip3 install --user -r requirements.txt

'''

import argparse
import logging
import os
from rich import print
from rich.logging import RichHandler

# Define the map to store AWS_REGION to RESOURCE_SHARE_ARN mappings
REGION_TO_ARN = {
    "us-east-2":
    "arn:aws:ram:us-east-2:852828256769:resource-share/495153f3-bc80-4c58-81fa-3b89b05833bc",
    "eu-central-1":
    "arn:aws:ram:eu-central-1:852828256769:resource-share/7031d4d2-c30d-4ee0-ac16-730543e3f191",
    # we can specific further regions and associate them with their ARN
}
AWS_REGION = ''


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Test for TGW ticket')
    parser.add_argument('-d', '--dest_account', help='Destination AWS account',
                        dest='dest_account', required=True)
    # parser.add_argument('-r', '--region', help='AWS Region',
    #    dest='region', required=True)
    parser.add_argument('-r', '--region', help='AWS Region',
                        required=True)
    parser.add_argument('--attach-tgw', dest='attach',
                        help='Attaches the destination VPC to the TGW',
                        action='store_true')
    parser.add_argument('--detach-tgw', dest='detach',
                        help='Detaches the destination VPC from the TGW',
                        action='store_true')

    args = parser.parse_args()

    if not args.detach and not args.attach:
        raise argparse.ArgumentTypeError(
            'Please set either --detach-tgw or --attach-tgw')

    return args


# Set up logging
FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.DEBUG, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

# Getting arguments
args = get_args()
print(args)
aws_region = args.region
os.environ['AWS_REGION'] = aws_region

if os.environ['AWS_REGION'] in REGION_TO_ARN:
    print('The Resource Share ARN for AWS_REGION %s: %s' %
          (os.environ['AWS_REGION'], REGION_TO_ARN[os.environ['AWS_REGION']]))
else:
    print('Error: AWS_REGION %s not found in REGION_TO_ARN' % os.environ['AWS_REGION'])
logging.info('Using AWS Region: %s' % aws_region)
