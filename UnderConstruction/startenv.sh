#!/bin/bash

export SERVERIP="64.227.43.55"
export CLIENTIP=`ifconfig tun0|grep "inet\ "|awk '{print $2}'`
export WORKDIR=`pwd`
mkdir $WORKDIR/enumeration
mkdir $WORKDIR/FootHold
mkdir $WORKDIR/Tools
mkdir $WORKDIR/IMG
touch follow.md
