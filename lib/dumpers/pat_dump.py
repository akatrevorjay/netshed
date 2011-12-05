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

def dump(test=False):
    (db, pipe) = get_pipe('pat', test=test)

    ip_port_regex = re.compile('\d+\.\d+\.\d+\.\d+/\d+')

    while True:
        line = pipe.readline()
        if not line:
            if test:
                break
            continue

        # parse fields and insert into mongodb
        try:
            pat = {}
            pat['line'] = line

            # get inside/outside ip/ports
            match = ip_port_regex.findall(line)
            if match:
                inside_ip_port = match[0].split('/')
                pat_ip_port = match[1].split('/')

                pat['pat_ip'] = ip2long(inside_ip_port[0])
                pat['pat_port'] = inside_ip_port[1]
                pat['ip'] = ip2long(pat_ip_port[0])
                pat['port'] = pat_ip_port[1]
            else:
                continue

            line = line.split(' ')
            try:
                line.remove('')
            except:
                pass

            # date in MMDD form
            pat['time'] = to_unix_timestamp(format_logdate(line[0] + ' ' + line[1]), line[2])

            # get date to know which collection to store to
            date = 'pat_' + str(datetime.datetime.now().year) + format_logdate(line[0] + ' ' + line[1])

            # log type (build/teardown)
            if line[5] == 'build' or line[5] == 'teardown':
                pat['log_type'] = line[5]

            coll = collection.Collection(db, date)
            coll.save(pat)

        except Exception as e:
            continue

if __name__ == '__main__':
    dump()
