#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
        echo 'This script must be run by root' >&2
        exit 1
fi

# Create Radios
modprobe mac80211_hwsim radios=2

# Create Network Namespaces
ip netns add supplicant

# Associate interfaces to namespaces
PHY1=$(basename $(readlink -f /sys/class/net/wlan1/phy80211))

iw phy $PHY1 set netns name supplicant

