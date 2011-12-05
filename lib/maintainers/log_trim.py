from utilities import get_config, get_date_x_days_ago, connect_db, get_log_types

def trim(test=False):
    """
    Implementation of a FIFO log window by trimming logs from X days ago from MongoDB
    by deleting old collections
    """

    # for every log type, delete the collection from a certain amount of days ago (in config)
    for log_type in get_log_types():

        try:
            oldest_date_to_keep = int(get_date_x_days_ago(int(get_config(log_type, 'window'))))
            db = connect_db(log_type, local=test, master=True)

            # grab every collection and if it's older than the log window, drop it
            for collection in db.collection_names():
                collection_date = collection[-8:]
                try:
                    if int(collection_date) < int(oldest_date_to_keep):
                        db.drop_collection(collection)
                except:
                    continue

        except Exception as e:
            print str(e)
            continue

if __name__ == '__main__':
    trim()
