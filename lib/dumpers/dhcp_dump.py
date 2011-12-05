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
    (db, pipe) = get_pipe('dhcp', test=test)
    m = "[a-f0-9][a-f0-9]"
    ip_regex = re.compile('\d+\.\d+\.\d+\.\d+')
    mac_regex = re.compile('%s:%s:%s:%s:%s:%s' % (m,m,m,m,m,m))
    via_ip_regex = re.compile('via (\d+\.\d+\.\d+\.\d+)')

    # read lines from named pipe
    while True:
        line = pipe.readline()
        if not line:
            if test:
                break
            continue

        # parse fields and insert into mongodb
        try:
            dhcp = {}
            dhcp['line'] = line
            # parse client ip
            match = ip_regex.search(line)
            if match:
                dhcp['ip'] = ip2long(match.group())

            # parse client mac
            match = mac_regex.search(line)
            if match:
                dhcp['mac'] = match.group().replace(':','')

            # parse via ip
            match = via_ip_regex.search(line)
            if match:
                dhcp['via_ip'] = ip2long(match.group(1))

            line = line.split(' ')

            try:
                line.remove('')
            except:
                pass

            # date in MMDD form
            dhcp['time'] = to_unix_timestamp(format_logdate(line[0] + ' ' + line[1]), line[2])

            # get date to know which collection to store to
            date = 'dhcp_' + str(datetime.datetime.now().year) + format_logdate(line[0] + ' ' + line[1])

            # log type (discover, ack, request, etc)
            log_type = line[5]
            if log_type[0] != 'b':
                dhcp['log_type'] = log_type.lower()
                if log_type[0] == 'D':
                    dhcp['log_type'] = dhcp['log_type'][4:]
            else:
                continue

            coll = collection.Collection(db, date)
            coll.save(dhcp)
        except Exception as e:
            print str(e)
            continue

if __name__ == '__main__':
    dump()
