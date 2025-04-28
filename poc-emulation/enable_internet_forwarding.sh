#!/bin/bash
set -e

# Interfaces that are used
INTERNET=$1
REPEATER=$2

# Enable DHCP client on the INTERNET interface
dhcpcd -n $INTERNET

# Configuring IP address of AP
ip addr del 192.168.0.1/24 dev $REPEATER 2> /dev/null || true
ip addr add 192.168.0.1/24 dev $REPEATER

# Enabling IP forwaring
sysctl net.ipv4.ip_forward=1 > /dev/null

# Enabling NAT
iptables -F
iptables -t nat -A POSTROUTING -o $INTERNET -j MASQUERADE
iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i $REPEATER -o $INTERNET -j ACCEPT
