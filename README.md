# netsec-krack-25

## Install dependencies
### Dependencies

```bash
sudo apt-get update
sudo apt-get install linux-headers-$(uname -r)
```
```bash
sudo apt update
sudo apt install build-essential checkinstall zlib1g-dev libnl-3-dev\
    libnl-genl-3-dev pkg-config libssl-dev net-tools git sysfsutils\
    python3-venv iw 
```
### Install Aircrack-ng
If `aircrack-ng` is not already installed into your machine (note that you'll also need `airmon-ng`) then you can build from source, here or anywhere you prefer in your machine:

```bash
wget https://download.aircrack-ng.org/aircrack-ng-1.7.tar.gz
tar -zxvf aircrack-ng-1.7.tar.gz
cd aircrack-ng-1.7
autoreconf -i
./configure --with-experimental
make
make install
ldconfig
```
### Install and Setup Pyenv
In repo we use both Python 3.12 and Python 2.7. In order to handle things easily, we decided touse pyenv in order to run Python 2.7 in a separate environment. In order to install Pyenv, follow the steps in <a href=https://github.com/pyenv/pyenv>https://github.com/pyenv/pyenv</a>, but **do it as a root**, as we will need to run some scripts with root permissions.


Now let's create a new environment containing Python 2.7.
```bash
sudo su
pyenv install 2.7.18
```

Eventually, we'll install some additional dependencies inside the newly created environment:
```bash
pyenv shell 2.7.18
pip install scapy==2.3.3 pycryptodome
pip install --user mitm_channel_based
```

In order to proceed, switch to the system version:
```bash
pyenv shell system
```

## Build
### Build Krackattack Scripts
```bash
cd krackattacks-scripts/krackattack
./build.sh
./pysetup.sh
```

After this, in order to make the scripts work, you should **disable hardware encryption**:
```bash
sudo ./disable-hwcrypto.sh
```
Then **reboot** the system.

### Build the rest
Run the following scripts (in the same order as below).
```bash
./build_openssl.sh
./build_wifi.sh
```
## Reference
<a href=https://www.krackattacks.com/>KRACK Official Website</a>
<a href=https://github.com/vanhoefm/krackattacks-scripts/tree/research/krackattack>Krack Scripts</a>
<a href=https://github.com/lucascouto/krackattack-all-zero-tk-key>Revisited KRACK POC</a>
