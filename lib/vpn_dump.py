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
    (db, pipe) = get_pipe('vpn', test=test)

    ip_regex = re.compile('\d+\.\d+\.\d+\.\d+')

    # read lines from named pipe
    while True:
        line = pipe.readline()
        if not line:
            if test:
                break
            continue

        # parse fields and insert into mongodb
        try:
            vpn = {}
            vpn['line'] = line
            vpn['log_type'] = 'packet'

            line = line.split(' ')
            try:
                line.remove('')
            except:
                pass

            vpn['time'] = to_unix_timestamp(format_logdate(line[0] + ' ' + line[1]), line[2])

            # get date to know which collection to store to
            date = 'vpn_' + str(datetime.datetime.now().year) + format_logdate(line[0] + ' ' + line[1])

            # using string functions to parse out standard lines with no errors
            if line[8] == 'User':
                vpn['group'] = line[7][1:-1].lower()
                vpn['username'] = line[9][1:-1].lower()
                vpn['ip'] = ip2long(line[11][1:-1])
            elif line[9] == 'Username':
                vpn['group'] = line[8][:-1].lower()
                vpn['username'] = line[11][:-1].lower()
                vpn['ip'] = ip2long(line[14][:-1])
            else:
                # failed / header invalid / no viable servers found / denied
                vpn['log_type'] = 'error'

                # parse group for 'no viable servers' lines
                if line[-2:-1][0] == 'tunnel-group':
                    vpn['group'] = line[-1:][0][1:-2].lower()

                line = ' '.join(line)

                match = ip_regex.search(line)
                if match:
                    vpn['ip'] = ip2long(match.group())
                try:
                    # try/except over if statement to limit overhead of regex
                    vpn['username'] = username_regex.search(line).group().lower()
                except:
                    pass

            coll = collection.Collection(db, date)
            coll.save(vpn)
        except:
            continue


if __name__ == '__main__':
    dump()
