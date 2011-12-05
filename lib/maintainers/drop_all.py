import sys
sys.path.append('../')
from pymongo import Connection, database
from optparse import OptionParser
from utilities import connect_db, get_config, get_log_types

def drop(user, password):
    """
    Drop every database and re-add net user account (CAREFUL BEFORE RUNNING)
    """

    connection = Connection(get_config('database', 'master_host'), int(get_config('database', 'port')))
    db = database.Database(connection, 'admin')
    db.authenticate(user, password)

    for log_type in get_log_types():
        try:

            db = database.Database(connection, log_type)

            print "dropping " + log_type
            connection.drop_database(log_type)

            # re-add net user account
            db.add_user(get_config('database', 'user'), get_config('database', 'password'))

        except Exception as e:
            print str(e)
            continue

if __name__ == '__main__':
    """ Takes root username and password """

    parser = OptionParser()
    parser.add_option("-u", "--user", dest="user")
    parser.add_option("-p", "--password", dest="password")
    (options, args) = parser.parse_args()

    drop(options.user, options.password)
