import sys
sys.path.append('../')
from utilities import get_log_types, connect_db, connect_collection
import pymongo
import optparse

# 'map' function in JavaScript
# emits (key, 1) for each key present in a document
map_fn = """
function () {
  for (key in this) {
    emit(key, 1);
  }
};
"""

# 'reduce' function in JavaScript
# totals the counts associated with a given key
reduce_fn = """
function (key, values) {
  var sum = 0;
  for each (value in values) {
     sum += value;
  }
  return sum;
};
"""

def get_key_frequencies(log_type, coll_name):
    """
    Prints statistics summarizing the frequency of each key
    in a collection of a Mongo database.  Helpful as a
    diagnostic tool.
    """
<<<<<<< Updated upstream

    # count all documents in this collection
    total = collection.count()
    #f or log_type in get_log_types():
=======
#    for log_type in get_log_types():
>>>>>>> Stashed changes
    for log_type in ['aruba']:

        # find all collections in the database
        database = connect_db(log_type, local=True)
        collnames = database.collection_names()
        try:
            collnames.remove('system.indexes')
            collnames.remove('system.users')
        except:
            pass

        # loop over collections names
        for collname in collnames:
            collection = connect_collection(log_type, collname, local=True)
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

    # use map/reduce to count the frequency of each field
    result = collection.map_reduce(map_fn, reduce_fn, "key_frequency")

<<<<<<< Updated upstream
    # print out the summary data
    print coll_name.center(60, '=')
    for item in result.find():
        key = item['_id']
        count = int(item['value'])
        freq = (count / float(total)) * 100.0
        print "    %-20.20s : %8i / %8i (%6.2f%%)" % (key, count, total, freq)
=======
            # use map/reduce to count the frequency of each field
            result = collection.map_reduce(map_fn, reduce_fn, 'results')

            # print out the summary data
            print collname.center(60, '=')
            for item in result.find():
                key = item['_id']
                count = int(item['value'])
                freq = (count / float(total)) * 100.0
                print "    %-20.20s : %8i / %8i (%6.2f%%)" % (key, count, total, freq)
>>>>>>> Stashed changes

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option("-l", "--log_type", help="type of log", default="dhcp", dest="log_type")
    parser.add_option("-c", "--collection", help="collection to aggregate", dest="collection")
    (options, args) = parser.parse_args()

    get_key_frequencies(options.log_type, options.collection)
