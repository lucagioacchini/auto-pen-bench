#!/bin/bash

#accept outcoming traffic
iptables  -P OUTPUT ACCEPT

# let packets from ongoing connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# drop all other packets
iptables -P INPUT   DROP
iptables -P FORWARD DROP