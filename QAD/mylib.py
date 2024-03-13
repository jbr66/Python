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

conv_oem_mdb = {
    'char': 'varchar',
    'integer': 'int',
    'decimal': 'decimal'
    }


if __name__ == '__main__':
    print(conv_oem_mdb)
    for k in conv_oem_mdb.keys():
        print('%s converted to %s' % (k, conv_oem_mdb[k]))
