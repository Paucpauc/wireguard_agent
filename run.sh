#!/bin/sh

modprobe wireguard

if ! lsmod | grep '^wireguard ' ; then
	apt-get update
	apt-get install -y linux-modules-$(uname -r) linux-headers-$(uname -r)
	modprobe wireguard
fi

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
		if ip l show dev $IFACE ; then
			exec wg_agent.py
		fi
	fi

fi
