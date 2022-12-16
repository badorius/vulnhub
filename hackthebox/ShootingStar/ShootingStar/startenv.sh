#!/bin/bash

export WORKDIR=$(pwd) 
export MACHINE=$(pwd|cut -f 8 -d "/")
export README=/home/darthv/git/badorius/vulnhub/README.md

export SERVERIP="64.227.43.55"
export CLIENTIP=$(ifconfig tun0|grep "inet\ "|awk '{print $2}')

! [ $(grep $MACHINE $README) ] && echo "" >> $README && echo "[$MACHINE](https://github.com/badorius/vulnhub/blob/main/hackthebox/$MACHINE/follow.md)" >> $README

mkdir $WORKDIR/enumeration
mkdir $WORKDIR/FootHold
mkdir $WORKDIR/Tools
mkdir $WORKDIR/IMG
mkdir $WORKDIR/Files
touch follow.md
