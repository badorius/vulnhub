#!/bin/bash

export SERVERIP="10.129.114.119"
export CLIENTIP=`ifconfig tun0|grep "inet\ "|awk '{print $2}'`
export WORKDIR=`pwd`
mkdir $WORKDIR/enumeration
mkdir $WORKDIR/FootHold
mkdir $WORKDIR/IMG
touch follow.md

