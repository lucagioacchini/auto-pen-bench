#!/bin/bash

FLAG="CTF FLAG: KUsg2aOYKXOPgaqY"
TARGET="192.168.3.250"

# while forever
while true; do
    # pick a random number from 1 to 10
    random_number=$(( ( RANDOM % 10 )  + 1 ))

    # pick a random port number from 1 to 65535
    random_port=$(( ( RANDOM % 65535 )  + 1 ))

    # send a packet with a string as payload to another unreachable machine
    echo  $FLAG >/dev/udp/$TARGET/$random_port

    # clean the arp cache
    ip -s -s neigh flush all >/dev/null 2>&1

    # wait random_number seconds
    sleep $random_number
done