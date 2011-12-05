import sys
sys.path.append('../')
from utilities import connect_db, get_log_types, connect_collection

def compact(test=False):
    """
    Compact (defrag/free) every collection
    """

    for log_type in get_log_types():
        try:
            db = connect_db(log_type, local=test, master=True)

            for coll_name in db.collection_names():
                coll = connect_collection(log_type, coll_name)
                try:
                    print "compacting " + coll_name
                    db.eval("db.runCommand({ compact : '%s'})" % (coll_name))
                except Exception as e:
                    print str(e)
                    continue

        except Exception as e:
            print str(e)
            continue

if __name__ == '__main__':
    compact()
