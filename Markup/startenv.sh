#!/bin/bash

export SERVERIP="10.129.159.28"
export CLIENTIP=`ifconfig tun0|grep "inet\ "|awk '{print $2}'`
export WORKDIR=`pwd`
mkdir $WORKDIR/enumeration
mkdir $WORKDIR/FootHold
touch follow.md

