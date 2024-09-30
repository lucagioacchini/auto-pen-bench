#!/bin/bash

#accept outcoming traffic
iptables  -P OUTPUT ACCEPT

# drop all other packets
iptables -P INPUT   DROP
iptables -P FORWARD DROP