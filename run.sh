#!/bin/sh

modprobe wireguard

lsmod | grep '^wireguard ' || (
apt-get update
apt-get install -y linux-modules-$(uname -r) linux-headers-$(uname -r)
modprobe wireguard
)

if [ -n "$IFACE" ] ; then

	ip link add dev $IFACE type wireguard
	if [ ! -e "/mnt/privatekey" ] ; then
		umask 0077
		wg genkey > /mnt/privatekey
	fi
	ip link set up dev $IFACE
	wg set $IFACE listen-port 60000 private-key /mnt/privatekey
	wg show $IFACE

	if [ -n "CONTROLLER" ] ; then
		exec wg_agent.py
	fi

fi
