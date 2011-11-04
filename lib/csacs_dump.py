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
    (db, pipe) = get_pipe('csacs', test=test)
    auth_regex = re.compile("Authen OK")
    ip_regex = re.compile('\d+\.\d+\.\d+\.\d+')
    mac_regex = re.compile("Caller-ID=([0-9A-Fa-f]+),")
    username_regex = re.compile(r"ONID\\\\([\w\d]+),")
    username2_regex = re.compile(r"User-Name=([\w\d\/]+),")

    # read in lines from named pipe
    while True:
        line = pipe.readline()
        if not line:
            if test:
                break
            continue
        try:
            # parse fields and insert into mongodb
            csacs = {}
            csacs['line'] = line
            split = line.split(' ')

            try:
                split.remove('')
            except:
                pass

            csacs['time'] = to_unix_timestamp(format_logdate(split[0] + ' ' + split[1]), split[2])

                       # get date to know which collection to store to
            date = 'csacs_' + str(datetime.datetime.now().year) + format_logdate(split[0] + ' ' + split[1])
            match = ip_regex.search(line)
            if match:
                csacs['ip'] = ip2long(match.group())

            match = mac_regex.search(line)
            if match:
                csacs['mac'] = match.group(1).lower()

            match = username_regex.search(line)
            if match:
                csacs['username'] = match.group(1).lower()
            else:
                match = username2_regex.search(line)
                if match:
                    csacs['username'] = match.group(1).lower()

            match = auth_regex.search(line)
            if match:
                csacs['log_type'] = 'authentication'

            coll = collection.Collection(db,date)
            coll.save(csacs)

        except Exception as e:
            continue

if __name__ == '__main__':
    dump()

