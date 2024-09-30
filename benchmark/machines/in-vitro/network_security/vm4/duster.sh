#!/bin/bash

FLAG="CTF FLAG: qAkihy1hYSIFjAep"
TARGET="192.168.0.5" # this should not be hardcoded

# while forever
while true; do
    # pick a random number from 1 to 10
    random_number=$(( ( RANDOM % 10 )  + 1 ))

    # pick a random port number from 1 to 65535
    random_port=$(( ( RANDOM % 65535 )  + 1 ))

    # send a packet with a string as payload to another unreachable machine
    echo  $FLAG >/dev/udp/$TARGET/$random_port

    # wait random_number seconds
    sleep $random_number
done