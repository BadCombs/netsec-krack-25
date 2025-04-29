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
### Install and Setup Conda
In repo we use both Python 3.12 and Python 2.7. In order to handle things easily, we decided touse Conda in order to run Python 2.7 in a separate environment. 
One way to install it is the following (otherwise check the <a href=https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html>website</a>): 
```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

We need to use Conda as root. So, we'll run `sudo su` before proceeding.
```bash
USER_HOME=$HOME
sudo su
source $USER_HOME/miniconda3/bin/activate
conda init --all
```
NOTE: After installing Conda, when opening a new session, it will automatically activate the `base` environment. In order to disable this behaviour, just run:
```bash
conda config --set auto_activate_base false
```

Now let's create a new environment containing Python 2.7.
```bash
sudo su
conda create -n krack-poc python=2.7
conda activate krack-poc
```

Eventually, we'll install some additional dependencies inside the newly created environment:
```bash
pip install scapy==2.3.3 pycryptodome
pip install --user mitm_channel_based
```

In order to proceed, exit from the environment:
```bash
conda deactivate
```

## Build
### Build Krackattak Scripts
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

### Build wpa_supplicant and hostapd
TODO
