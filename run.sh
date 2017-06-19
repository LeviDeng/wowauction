#!/bin/bash
START='nohup python getdata.py &'
STOP='ps aux|grep pythpn|grep wowAuction|grep -v grep|awk -F" "  "{print $2}"'
case $1 in
start)
	$START;;
stop)
	$STOP;;
esac
