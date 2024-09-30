#!/bin/bash

#accept outcoming traffic
iptables  -P OUTPUT ACCEPT

# loopback traffic
iptables -A INPUT -i lo -j ACCEPT

# accept incoming traffic to fake server
iptables -A INPUT -i eth0 -p tcp --dport 22 -j ACCEPT

# let packets from ongoing connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# drop all other packets
iptables -P INPUT   DROP
iptables -P FORWARD DROP