#!/usr/bin/python
# Copyright (c) 2011 Oregon State University - Network Engineering
# All rights reserved.
#
# @author: Kevin Ngo <kevin.ngo@oregonstate.edu>

from pymongo import Connection, database, collection
from utilities import *
import datetime
import re

def dump(test=False):
    (db, pipe) = get_pipe('named', test=test)

    zone_regex = re.compile('([\w\d\.]+)/\w')

    # read lines from named pipe
    while True:
        line = pipe.readline()
        if not line:
            if not line:
                break
            continue

        # parse fields and insert into mongodb
        try:

            named = {}
            named['line'] = line

            match = zone_regex.search(line)
            if match:
                named['zone'] = match.group(1).lower()

            line = line.split(' ')

            # date in MMDD form
            named['time'] = to_unix_timestamp(format_logdate(line[0] + ' ' + line[1]), line[2])

            # get date to know which collection to store to
            date = 'named_' + str(datetime.datetime.now().year) + format_logdate(line[0] + ' ' + line[1])
            if not 'zone' in named:
                if line[-2] == 'zone':
                    named['zone'] = line[-1][1:-2].lower()
                else:
                    if '.' in line[-1]:
                        named['zone'] = line[-1][0:-1]

            coll = collection.Collection(db, date)
            coll.save(named)

        except:
            continue

if __name__ == '__main__':
    dump()
