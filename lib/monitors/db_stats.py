import sys
sys.path.append('../')
from utilities import connect_db, connect_collection, get_log_types

def get_stats():

    for log_type in get_log_types():

        db = connect_db(log_type)
        log_stats = db.command("dbstats")

        stats_coll = connect_collection('tools', 'db_stats')
        stats_object = stats_coll.update({'db':log_type}, log_stats, upsert=True)
        #stats_coll.save(log_stats)

if __name__ == '__main__':
    get_stats()
