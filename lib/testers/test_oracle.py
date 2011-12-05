import sys
sys.path.append('../')
import cca_dump
import csacs_dump
import dhcp_dump
import greylist_dump
import header_reject_dump
import named_dump
import nat_dump
import pat_dump
import resnet_dump
import vpn_dump
from utilities import connect_db, connect_collection
from pymongo import collection, Connection , database
import unittest

class TestDump(unittest.TestCase):

    def setUp(self):
        self.dbs =  ['cca','csacs','dhcp','greylist','header_reject','named','nat','pat','resnet','vpn']
        self.dumpers = [cca_dump, csacs_dump, dhcp_dump, greylist_dump, header_reject_dump,
                        named_dump, nat_dump, pat_dump, resnet_dump, vpn_dump]
        self.queries = [{"username":'testing'}, {"mac" : "aabbccddeeff"}, {"recipient" : "bob.alice@onid.orst.edu"}, {"from_addr" : "trentbob@yahoo.com"}, {"zone" : "osupachyderm.org"},{"time" : 1319029072}, {"port" : "60940"}, {"username" : "alice"}]
        self.test_keys =  ['username','mac','recipient','from_addr','zone','time','port','ip']
        self.test_list =  [{'dumper': cca_dump,          'logtype': 'cca'},
                           {'dumper': csacs_dump,        'logtype': 'csacs'},
                           {'dumper': dhcp_dump,         'logtype': 'dhcp'},
                           {'dumper': greylist_dump,     'logtype': 'greylist'},
                           {'dumper': header_reject_dump,'logtype': 'header_reject'},
                           {'dumper': named_dump,        'logtype': 'named'},
                           {'dumper': nat_dump,          'logtype': 'nat'},
                           {'dumper': pat_dump,          'logtype': 'pat'},
                           {'dumper': resnet_dump,       'logtype': 'resnet'},
                           {'dumper': vpn_dump,          'logtype': 'vpn'}]

        for case in self.test_list:
            db = connect_db(case['logtype'], local=True)
            names = db.collection_names()
            try:
                names.remove("system.indexes")
            except:
                pass

    def tests(self):
        for case in self.test_list:
            case['dumper'].dump(test=True)
            names = connect_db(case['logtype'], local=True).collection_names()
            coll = None
            names.remove('system.indexes')
            try:
                coll = connect_collection(case['logtype'], names[0], local=True)
                self.assertEqual(coll.count() % 5, 0)
                for test in self.test_keys:
                    assert coll.distinct(test) is not 0
            except Exception as e:
                print case['logtype'] + ' had an error'
                print str(e)
                pass

suite = unittest.TestLoader().loadTestsFromTestCase(TestDump)
unittest.TextTestRunner(verbosity=2).run(suite)
