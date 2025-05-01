#!/bin/bash

# KRACK Attack Simulation Launcher
# -------------------------------
# This script launches all components of the KRACK attack simulation:
# 1. The Access Point (server.py)
# 2. The Client (client.py)
# 3. The MITM Attacker (mitm.py)

VENV_DIR="./venv"
VENV_PYTHON="$VENV_DIR/bin/python"

# Configuration
SERVER_TERM_TITLE="Authenticator Access Point"
CLIENT_TERM_TITLE="Supplicant Wifi Client"
ATTACKER_TERM_TITLE="MITM Attacker"
TERMINAL="xterm" 

if [ -d "$VENV_DIR" ]; then
  echo "Activating virtual environment in $VENV_DIR..."
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"
else
  echo "ERROR: Virtual environment not found at $VENV_DIR."
  echo "Please create it with: python3 -m venv $VENV_DIR"
  exit 1
fi

clear

echo "Starting WPA2 Access Point..."
$TERMINAL -T "$SERVER_TERM_TITLE" -geometry 100x30+0+0 -e "python3 authenticator.py; echo $'\nPress Enter to close...'; read" &

sleep 1

echo "Starting MITM Attacker..."
$TERMINAL -T "$ATTACKER_TERM_TITLE" -geometry 100x30-0+0 -e "python3 mitm.py; echo $'\nPress Enter to close...'; read" &

sleep 1

echo "Starting WiFi Client..."
$TERMINAL -T "$CLIENT_TERM_TITLE" -geometry 100x30+0-0 -e "python3 supplicant.py; echo $'\nPress Enter to close...'; read" &

wait

