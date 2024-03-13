#!/usr/bin/env python3
'''
NAME
    mylib.py    -   Library with functions for conversion oemdb -> mariadb

AUTHOR
    Written by John Brink (j6b@qad.com)

REVISION HISTORY
---------------------------------------------------------------------------
    0.1 03/13/2024  j6b - Initial version
---------------------------------------------------------------------------
vim: ts=4
'''

conv_oem_mdb = [
    ('character', 'varchar'),
    ('character', 'text'),
    ('clob', 'longtext'),
    ('varchar', 'text'),
    ('double precision', 'double'),
    ('logical', 'tinyint'),
    ('integer', 'int'),
    ('int64', 'bigint'),
    ('date', 'date'),
    ('decimal', 'decimal'),
    ('numeric', 'decimal'),
    ('real', 'float'),
    ]


if __name__ == '__main__':
    print('%40s' % 'Datatypes'.center(40))
    print('%-20s %-20s' % ('Progress','MariaDB'))
    print(40*'-')
    for k,v in conv_oem_mdb:
        if v == 'text':
            print('%-20s %-20s when larger than 255' % (k, v))
        else:
            print('%-20s %-20s' % (k, v))
