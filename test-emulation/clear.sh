#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
        echo 'This script must be run by root' >&2
        exit 1
fi

# Remove Network Namespaces
ip netns del supplicant

# Remove Radios
modprobe -r mac80211_hwsim

