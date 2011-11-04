from utilities import get_config, get_date_x_days_ago, connect_db

def trim(test=False):
    """
    Implementation of a FIFO log window by trimming logs from X days ago from MongoDB
    by deleting old collections
    """

    log_types = ('cca', 'csacs', 'dhcp', 'greylist', 'header_reject', 'named', 'nat', 'pat', 'resnet', 'vpn')

    # for every log type, delete the collection from a certain amount of days ago (in config)
    for log_type in log_types:
        try:
            coll_name = log_type + '_' + get_date_x_days_ago(int(get_config(log_type, 'window')))
            db = connect_db(log_type, local=test, master=True)
            db.drop_collection(coll_name)
        except Exception as e:
            print str(e)
            continue

if __name__ == '__main__':
    trim()
