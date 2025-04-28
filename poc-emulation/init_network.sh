#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
        echo 'This script must be run by root' >&2
        exit 1
fi

# Create Radios
modprobe mac80211_hwsim radios=4

# Create Network Namespaces
ip netns add supplicant
ip netns add hostapd

# Associate interfaces to namespaces
PHY0=$(basename $(readlink -f /sys/class/net/wlan0/phy80211))
PHY1=$(basename $(readlink -f /sys/class/net/wlan1/phy80211))

iw phy $PHY0 set netns name hostapd
iw phy $PHY1 set netns name supplicant

ip link set dev eth1 netns hostapd

airmon-ng check kill
