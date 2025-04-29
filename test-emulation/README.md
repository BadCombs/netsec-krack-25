# Client Test (Emulation with mac80211_hwsim)

## Initialise the Network Emulation


```bash
sudo ./init_network.sh
```

## Connection and Testing
### Start the Test
Open a new Terminal session in `../krackattacks-scripts/krackattack/'. Run:

```bash
sudo su
rfkill unblock wifi
source venv/bin/activate
```

```bash
./krack-test-client.py
```

### Start the DHCP client on the Supplicant interface
```bash
sudo ip netns exec supplicant dhcpcd -n wlan1
```

### Start a non-vulnerable Supplicant
Open a new Terminal session in this folder and run:
```bash
sudo ip netns exec supplicant wpa_supplicant -D nl80211 -i wlan1 -c supplicant_test.conf
```

### Start the vulnerable Supplicant
```bash
sudo su
source init_env_sup
ip netns exec supplicant ./wpa_supplicant-2.4 -D nl80211 -i wlan1 -c supplicant_test.conf
```

### NOTE!
When restarting the Test script remove the created Virtual Interface. For example, if its name is `monwlan0`, the execute:
```bash
sudo iw dev monwlan0 del
```

## Deinitialise the Network Emulation
```bash
sudo ./clear.sh
```
