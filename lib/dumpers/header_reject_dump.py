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
    (db, pipe) = get_pipe('header_reject', test=test)

    email_regex = re.compile('[\w\d\.]+@[\w\d\.]+')

    # read lines from named pipe
    while True:
        line = pipe.readline()
        if not line:
            if test:
                break
            continue

        # parse fields and insert into mongodb
        try:

            header_reject = {}
            header_reject['line'] = line
            emails = email_regex.findall(line)
            if emails:
                header_reject['from_addr'] = emails[0].lower()
                header_reject['to_addr'] = [email for email in emails if email != emails[0]]

            line = line.split(' ')
            try:
                line.remove('')
            except:
                pass
            # date in MMDD form
            header_reject['time'] = to_unix_timestamp(format_logdate(line[0] + ' ' + line[1]), line[2])

            # get date to know which collection to store to
            date = 'header_reject_' + str(datetime.datetime.now().year) + format_logdate(line[0] + ' ' + line[1])

            coll = collection.Collection(db, date)
            coll.save(header_reject)

        except:
            continue

if __name__ == '__main__':
    dump()
