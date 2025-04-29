#!/bin/bash

# Build wpa_supplicant
cd ./wpa_supplicant-2.4/wpa_supplicant/
CFLAGS="-I../../opt/openssl-1.0.2l/include" LDFLAGS="-L../../opt/openssl-1.0.2l/lib" make

# Build hostapd
cd ../../hostapd-2.4/hostapd/
CFLAGS="-I../../opt/openssl-1.0.2l/include" LDFLAGS="-L../../opt/openssl-1.0.2l/lib" make
