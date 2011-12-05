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

def dump(test=False):
    (db, pipe) = get_pipe('greylist',test=test)

    # read lines from named pipe
    while True:
        line = pipe.readline()
        if not line:
            if test:
                break
            continue

        # parse fields and insert into mongodb
        try:
            greylist = {}
            greylist['line'] = line
            split = line.split(' ')
            try:
                split.remove('')
            except:
                pass

            # date in MMDD form
            greylist['time'] = to_unix_timestamp(format_logdate(split[0] + ' ' + split[1]), split[2])

            # get date to know which collection to store to
            date = 'greylist_' + str(datetime.datetime.now().year) + format_logdate(split[0] + ' ' + split[1])
            line = line.split('<')

            # ip
            greylist['ip'] = ip2long(line[-1][0:-2])

            # recipient address
            greylist['recipient'] = line[-3].split(' ')[0][0:-1]

            # sender address
            greylist['sender'] = line[-2].split(' ')[0][0:-1]
            coll = collection.Collection(db,date)
            coll.save(greylist)

        except:
            continue

if __name__ == '__main__':
    dump()
