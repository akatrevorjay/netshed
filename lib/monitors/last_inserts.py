import sys
sys.path.append('../')
from utilities import connect_db, connect_collection, get_log_types
from pymongo import DESCENDING

def print_last_inserts():
    """ return time of last insert for each logtype """

    for log_type in get_log_types():

        newest_coll_name = connect_db(log_type, local=False).collection_names()[-1]
        coll = connect_collection(log_type, newest_coll_name, local=False)

        for document in coll.find().sort([('time', DESCENDING)]).limit(1):
            line = document['line'].split(' ')
            try:
                line.remove('')
            except:
                pass
            print log_type + '\t\t' + str(line[0:3])

if __name__ == '__main__':
    print_last_inserts()
