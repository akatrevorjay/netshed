#!/bin/bash
# Starts all the log dumpers and kills them all if this gets killed 
# Takes a few seconds to die due to sleep 

function setTrap {
    trap killDumpers TERM SIGINT SIGTERM
}

function killDumpers {
    kill ${dhcp_pid}
    kill ${cca_pid} 
    kill ${named_pid} 
    kill ${vpn_pid} 
    kill ${greylist_pid} 
    kill ${header_reject_pid}
    exit
}

setTrap

python dhcp_dump.py &
dhcp_pid=$!

python cca_dump.py &
cca_pid=$!

python named_dump.py &
named_pid=$!

python vpn_dump.py &
vpn_pid=$!

python greylist_dump.py &
greylist_pid=$!

python header_reject_dump.py &
header_reject_pid=$!

while true; do
    sleep 10
done

