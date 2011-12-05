#!/bin/bash
# Starts all the log dumpers and kills them all if this gets killed
# Takes a few seconds to die due to sleep

function setTrap {
    trap killDumpers TERM SIGINT SIGTERM
}

function killDumpers {
    kill ${pat_pid}
    kill ${nat_pid}
    kill ${csacs_pid}
    kill ${resnet_pid}
    exit
}

setTrap

python pat_dump.py &
pat_pid=$!

python nat_dump.py &
nat_pid=$!

python csacs_dump.py &
csacs_pid=$!

python resnet_dump.py &
resnet_pid=$!

while true; do
    sleep 5
done

