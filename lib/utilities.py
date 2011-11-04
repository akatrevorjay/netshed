from pymongo import Connection, database, collection
import mongoengine
import ConfigParser
import datetime
import time
import os
import re

def connect_db(db_name, local=False, master=False):
    """ Connect to db, returns db object """

    if local:
        connection = Connection('localhost', 27017)
        return database.Database(connection, db_name)

    host = get_config('database', 'host')
    if master:
        host = get_config('database', 'master_host')
    port = int(get_config('database', 'port'))
    user = get_config('database', 'user')
    password = get_config('database', 'password')

    connection = Connection(host, port)
    db_connect = database.Database(connection, db_name)
    db_connect.authenticate(user, password)
    return db_connect

def get_pipe(logtype, test=False):
    """Takes a logtype and testing flag and returns a db and a pipe"""
    db = connect_db(logtype, local = test, master = True)
    pipe =  open(get_config(logtype, 'pipe', test=test), 'r')
    return db, pipe

def connect_collection(db_name, collection_name, local=False):
    """ Connect to DB and get collection, return collection object
        for small scope use """

    if local:
        connection = Connection('localhost', 27017)
        db_connect = database.Database(connection, db_name)
        return collection.Collection(db_connect, collection_name)

    host = get_config('database', 'host')
    port = int(get_config('database', 'port'))
    user = get_config('database', 'user')
    password = get_config('database', 'password')

    connection = Connection(host, port)
    db_connect = database.Database(connection, db_name)
    db_connect.authenticate(user, password)

    return collection.Collection(db_connect, collection_name)

def pymongo_query(query, logtype, local=False):
    """ generic Django view for netshed, takes in query dictionary
        and type of log and returns the resulting lines of logs"""

    loglines = []
    collections = []

    if 'limit' in query:
        limit = int(query['limit'])

    # pymongo raw query
    if 'date' in query:

        if query['date'] == 'all':
            collections = connect_db(logtype, local).collection_names()
        else:
            collections.append(logtype + '_' + query['date'])
            try:
                # search two days if start time > end time
                if span_two_days(query['start_hr'], query['start_min'], query['end_hr'], query['end_min']):
                    collections.append(logtype + increment_date(query['date']))
            except KeyError:
                pass

        # get collection object for each collection to search on and query
        for collection in collections:
            collection = connect_collection(logtype, collection, local)

            results = [log for log in collection.find(format_query_input(query)).limit(limit)]
            results = sorted(results, key=lambda log:log['time'])
            loglines += [log['line'] for log in results]

    return loglines

def connect_mongo_session(local=False):
    """ Connect to database via mongoengine for django session """

    if local:
        mongoengine.connect('tools', host='localhost', port=27017)
    else:
        host = get_config('database', 'master_host')
        port = int(get_config('database', 'port'))
        user = get_config('database', 'user')
        password = get_config('database', 'password')
        mongoengine.connect('tools', username=user, password=password, host=host, port=port)

def date_to_timestamp_range(date):
    """ YYYYMMDD to two unix timestamps of start and end of given date """
    start_time = int(time.mktime(time.strptime(date, "%Y%m%d")))
    end_time = start_time + 86400
    return [start_time, end_time]

def follow(logfile):
    """
    Used in development
    Tail follow a file using generators to return values on the fly
    """
    fd = open(logfile)
    #fd.seek(0,2) # go to EOF
    while True:
        line = fd.readline()
        if line:
            yield line
        yield None

def format_logdate(logdate):
    """ Formats "MMM DD" to "MMDD" """
    dates = {'JAN':'01', 'FEB':'02', 'MAR':'03', 'APR':'04', 'MAY':'05',
             'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09', 'OCT':'10',
             'NOV':'11', 'DEC':'12'}

    logdate = logdate.split(' ')
    return dates[str(logdate[0]).upper()] + "%02d" % int(logdate[1])

def format_query_input(query):
    """ used to be able to pass in query dictionary to mongo as raw query """

    # make mac lowercase and strip of colons
    if 'mac' in query:
        query['mac'] = query['mac'].lower().replace(':','')
    # convert ip to long
    if 'ip' in query:
        query['ip'] = ip2long(query['ip'])
    # for greylist logs where there is a mongo search and mysql search options
    if 'search' in query:
        del(query['search'])
    # return portion of array
    if 'limit' in query:
        del(query['limit'])
    # parse date and time inputs
    return format_time(query)

def format_query_output(query):
    """ Forms query dict to a pretty string """
    query = format_query_input(query)
    if len(query) is 0:
        return None
    if 'ip' in query:
        query['ip'] = long2ip(query['ip'])
    if 'time' in query:
        query['time'] = seconds_to_timestamp(query['time']['$gte']) + ' to ' + seconds_to_timestamp(query['time']['$lt'])
    string = '[ '
    for key,value in query.items():
        string += "%s: %s | " % (key,value)
    string = string[0:-2] + ']'
    return string

def increment_date(date):
    """takes a date and increments it and returns a string formmated YYYYMMDD"""
    date = str(date)
    current = datetime.date(int(date[:4]),int(date[4:6]),int(date[-2:]))
    current += datetime.timedelta(days = 1)
    return str(current.year)+str(current.month)+str(current.day)

def span_two_days(start_hr, start_min, end_hr, end_min):
    """Determines if the times span two days which means start time > end time"""
    if (int(start_hr) == int(end_hr) and int(start_min) > int(end_min)) or int(end_hr) < int(start_hr):
        return True
    else:
        return False

def format_time(query):
    """ big piece of user input handling...takes query and formats date/time to a mongodb raw query """

    # parse user input for time field
    time_error = 0
    fields = ['start_hr', 'start_min', 'end_hr', 'end_min']
    for field in fields:
        try:
            if 'hr' in field:
                if int(query[field]) < 0 or int(query[field]) > 24:
                    del(query[field])
            if 'min' in field:
                if int(query[field]) < 0 or int(query[field]) > 60:
                    del(query[field])
        except KeyError, ValueError:
            try:
                del(query[field])
            except KeyError:
                pass

    # turns a date into a range of unix seconds for db to compare
    if 'date' in query:
        if query['date'] != 'all':
            second_range = date_to_timestamp_range(query['date'])
            start = second_range[0]

            # if start time was given, add it to the date (seconds)
            if 'start_hr' in query:
                if not 'start_min' in query:
                    query['start_min'] = '00'
                second_range[0] = second_range[0] + int(query['start_hr']) * 3600
                second_range[0] = second_range[0] + int(query['start_min']) * 60
                del(query['start_hr'])
                del(query['start_min'])

            # if end time was given, add it to the date (seconds)
            if 'end_hr' in query:
                if not 'end_min' in query:
                    query['end_min'] = '00'
                second_range[1] = start + int(query['end_hr']) * 3600
                second_range[1] = second_range[1] + int(query['end_min']) * 60
                del(query['end_hr'])
                del(query['end_min'])

            # if start time is greater than end time, roll over the endtime to next day
            if second_range[0] > second_range[1]:
                second_range[1] += 86400
            query['time'] = {'$gte': second_range[0], '$lt': second_range[1]}
            del(query['date'])
        else:
            for field in fields:
                try:
                    del(query[field])
                except KeyError:
                    pass

    return query

def get_config(type, field, test=False):
    """ Get values from the config file """
    config = ConfigParser.ConfigParser()
    if test:
        config.read('mongo_dump.cfg')
        value = config.get(type, field)
    try:
        config.read("/data/www/netshed/lib/mongo_dump.cfg") #spot
        value =  config.get(type, field)
    except:
        config.read("/usr/local/lib/python2.6/dist-packages/netshed/lib/mongo_dump.cfg") #astro
        value = config.get(type, field)
    return value

def get_log_window(logtype, local=False):
    """
    Returns dates in which there are logs for
    """
    db_conn = connect_db(logtype, local)
    collections = db_conn.collection_names()

    dates = []
    for collection in collections:
        try:
            dates.append(int(collection[-8:]))
        except ValueError:
            pass
    return dates

def ip2long(ip):
    """ converts ip to integer format """
    if not ip:
        return None
    try:
        (o1, o2, o3, o4) = ip.split('.')
        return ((int(o1) * 16777216) + (int(o2) * 65536) + \
                (int(o3) * 256) + int(o4))
    except Exception:
        return None

def long2ip(long):
    """ converts integer ip to dots and decimals """
    if not long or not re.match("^\d+$", str(long)):
        return None
    try:
        o1 = long / 2**(8*3)
        long -= (o1 * 2**(8*3))
        o2 = long / 2**(8*2)
        long -= (o2 * 2**(8*2))
        o3 = long / 2**8
        o4 = long - (o3 * 2**8)
        return ("%d.%d.%d.%d" % (o1, o2, o3, o4))
    except:
        return None

def get_date_x_days_ago(days_to_subtract):
    """ get the date X days ago in YYYYMMDD """
    date = datetime.date.today() - datetime.timedelta(days=days_to_subtract)
    return '%04d%02d%02d' % (date.year, date.month, date.day)

def to_unix_timestamp(date, time_string):
    """ MMDD HH:MM:SS to Unix time"""
    year = datetime.datetime.now().year
    date = str(year) + date
    return time.mktime(time.strptime(date + ' ' + time_string, "%Y%m%d %H:%M:%S"))

def seconds_to_timestamp(seconds):
    """ unix timestamp to human readable """
    seconds = float(seconds)
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(seconds))


