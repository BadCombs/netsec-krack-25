#!/bin/bash

NETSEC_DIR=$PWD

# Build openssl-1.1.1k
cd ./openssl-1.1.1k
./config --prefix=$NETSEC_DIR/opt/openssl-1.1.1k --openssldir=$NETSEC_DIR/opt/openssl-1.1.1k shared zlib && make && make install
