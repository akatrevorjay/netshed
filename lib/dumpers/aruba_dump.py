#!/usr/bin/python
# Copyright (c) 2011 Oregon State University - Network Engineering
# All rights reserved.
#
# @author: Ian Fridge <fridgei@oregonstate.edu>

from pymongo import Connection, database, collection
import datetime
import re
import sys
sys.path.append('../')
from utilities import *

def dump(test=False):
    (db, pipe) =  get_pipe('aruba', test=test)

    # Regular expression for finding IP addresses
    ip_regex = re.compile('\d+\.\d+\.\d+\.\d+')

    # Regular expression for finding mac addresses
    m = '[a-f0-9][a-f0-9]'
    mac_regex = re.compile('%s:%s:%s:%s:%s:%s' % (m,m,m,m,m,m))

    # Regular expression for finding the location of an aruba access point
    location_regex = re.compile('aru-(\w-*\/*)*')

    #this will be replaced with a while True so it runs forever
    while True:
        try:
            line = pipe.readline()
            if not line:
                continue

            aruba = {}
            aruba['line'] = line

            # In case of extra spaces in the log try to remove them
            split = line.split(' ')
            try:
                split.remove('')
            except:
                pass

            # Get the time and date at the start of the line and which switch is involved
            aruba['time'] = to_unix_timestamp(format_logdate(split[0] + ' ' + split[1]), split[2])
            date = 'aruba_' + str(datetime.datetime.now().year) + format_logdate(split[0] + ' ' + split[1])

            # The name of the aruba switch is found in index 3
            aruba['aruba'] = split[3]

            # Find all the ip addresses and convert them to longs
            match = ip_regex.findall(line)
            try:
                for i in range(len(match)):
                    match[i] = ip2long(match[i])
            except:
                pass
            aruba['ip'] = match

            # Get the mac addresses and location.  Some don't have locations so we use a try except
            match =  mac_regex.findall(line)
            for i in range(len(match)):
                match[i] = match[i].replace(':','')

            if len(match[i]) != 0:
                aruba['mac'] = match

            # Get the location of the switch
            match = location_regex.search(line)
            try:
                aruba['location'] = match.group(0)
            except:
                pass

            # The logtype is always stored at index 7
            logtype = split[7]
            if logtype == '<warn>':
                aruba['type'] = 'warning'
            elif logtype == '<noti>':
                aruba['type'] = 'notification'
            else:
                aruba['type'] = 'error'

            # Send those bastards to mongodb
            coll = collection.Collection(db,date)
            coll.save(aruba)

	except:
            continue

if __name__ == '__main__':
    dump()
