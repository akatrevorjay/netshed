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
from utilities import connect_db
from pymongo import collection, Connection , database


if __name__ == '__main__':
    dumpers = [cca_dump, csacs_dump, dhcp_dump, greylist_dump, header_reject_dump,
              named_dump, nat_dump, pat_dump, resnet_dump, vpn_dump]
    for dumper in dumpers:
        dumper.dump(test=True)
