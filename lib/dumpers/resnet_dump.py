#!/usr/bin/python
# Copyright (c) 2011 Oregon State University - Network Engineering
# All rights reserved.
#
# @author: Kevin Ngo <kevin.ngo@oregonstate.edu>

import sys
sys.path.append('../')
from pymongo import Connection, database, collection
from utilities import *
import datetime
import re

def dump(test = False):
    (db, pipe) = get_pipe('resnet', test=test)

    # read from named pipe
    while True:
        line = pipe.readline()
        if not line:
            if test:
                break
            continue

        # parse fields and insert into mongodb
        try:
            resnet = {}
            resnet['line'] = line
            line = line.split(' ')
            try:
                line.remove('')
            except:
                pass

            # date in MMDD form
            resnet['time'] = to_unix_timestamp(format_logdate(line[0] + ' ' + line[1]), line[2])

            # get date to know which collection to store to
            date = 'resnet_' + str(datetime.datetime.now().year) + format_logdate(line[0] + ' ' + line[1])

            resnet['username'] = line[5].split('=')[1]
            resnet['ip'] = ip2long(line[6].split('=')[1])
            resnet['mac'] = line[7].split('=')[1].replace(':','')

            coll = collection.Collection(db, date)
            coll.save(resnet)
        except:
            continue

if __name__ == '__main__':
    dump()
