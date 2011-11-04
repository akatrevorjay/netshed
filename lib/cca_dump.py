#!/usr/bin/python
# Copyright (c) 2011 Oregon State University - Network Engineering
# All rights reserved.
#
# @author: Kevin Ngo <kevin.ngo@oregonstate.edu>

from utilities import *
from pymongo import Connection, database, collection
import datetime
import re

def dump(test=False):
    (db, pipe) = get_pipe('cca', test=test)
    m = '[a-f0-9][a-f0-9]'
    ip_regex = re.compile('\d+\.\d+\.\d+\.\d+')
    mac_regex = re.compile('%s:%s:%s:%s:%s:%s' % (m,m,m,m,m,m))
    user_kick_regex = re.compile('User:(\w+)')
    user_logout_regex = re.compile('user (\w+)\n')
    user_exists_regex = re.compile(':(\w+) user account')

    # read in lines from named pipe
    while True:
        line = pipe.readline()
        if not line:
            if test:
                break
            continue

        # parse fields and insert into mongodb
        try:
            cca = {}
            cca['line'] = str(line)
            split = line.split(' ')

            try:
                split.remove('')
            except:
                pass

            cca['time'] = to_unix_timestamp(format_logdate(split[0] + ' ' + split[1]), split[2])

             # get date to know which collection to store to
            date = 'cca_' + str(datetime.datetime.now().year) + format_logdate(split[0] + ' ' + split[1])

            # parse standard cca authentication line
            if split[5][15] == '[':
                cca['log_type'] = 'authentication'
                cca['ip'] = ip2long(split[7][:-1])
                cca['mac'] = split[5][16:].lower().replace(':','')
                cca['username'] = split[8].lower()

            # parse miscellaneous lines (possibly unnecessary)
            else:
                match = ip_regex.search(line)
                if match:
                    cca['ip'] = ip2long(match.group())

                match = mac_regex.search(line)
                if match:
                    cca['mac'] = match.group().lower().replace(':','')

                match = user_kick_regex.search(line)
                if match:
                    cca['username'] = match.group(1).lower()

                match = user_logout_regex.search(line)
                if match:
                    cca['username'] = match.group(1).lower()

                match = user_exists_regex.search(line)
                if match:
                    cca['username'] = match.group(1).lower()

            coll = collection.Collection(db, date)
            coll.save(cca)

        except Exception as e:
            continue


if __name__ == '__main__':
    dump()

