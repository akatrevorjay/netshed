#!/usr/bin/python
# Copyright (c) 2011 Oregon State University - Network Engineering
# All rights reserved.
#
# @author: Kevin Ngo <kevin.ngo@oregonstate.edu>

from pymongo import Connection, database, collection
from utilities import *
import datetime

def dump(test=False):
    (db, pipe) = get_pipe('nat', test=test)

    while True:
        line = pipe.readline()
        if not line:
            if test:
                break
            continue

        # parse fields and insert into mongodb
        try:
            nat = {}
            nat['line'] = line
            line = line.split(' ')
            try:
                line.remove('')
            except:
                pass

            # get natted/outside ips
            nat['nat_ip'] = ip2long(line[12][:-2])
            nat['ip'] = ip2long(line[13][:-2])

            # date in MMDD form
            nat['time'] = to_unix_timestamp(format_logdate(line[0] + ' ' + line[1]), line[2])

            # get date to know which collection to store to
            date = 'nat_' + str(datetime.datetime.now().year) + format_logdate(line[0] + ' ' + line[1])


            # log type (created/deleted)
            if line[10] == 'Created' or line[10] == 'Deleted':
                nat['log_type'] = line[10]

            coll = collection.Collection(db, date)
            coll.save(nat)

        except:
            continue

if __name__ == '__main__':
    dump()
