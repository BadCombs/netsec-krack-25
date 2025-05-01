#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
        echo 'This script must be run by root' >&2
        exit 1
fi

# Check argument
if [ "$#" -ne 1 ]; then
    echo "Usage: sudo ./$0 <Internet Interface for Hostapd>"
fi

# Reassign eth to root namespace
ip netns exec hostapd ip link set $1 netns 1

# Remove Network Namespaces
ip netns del supplicant
ip netns del hostapd

# Remove Radios
modprobe -r mac80211_hwsim

systemctl start NetworkManager
