#!/usr/bin/python3

import os
import json
import requests
import socket
import time
import subprocess
import re
import sys

iface = os.environ['IFACE']
url = os.environ['CONTROLLER']

def get_pubkey():
    out = subprocess.check_output(["wg","show",iface])
    return re.search(r'^\s*public key:\s+(\S+)', out.decode("utf-8"),re.MULTILINE).group(1)


def get_ips():
    out = subprocess.check_output(["ip","-4","-o","a","show","dev",iface])
    return re.findall(r'inet (\d+\.\d+\.\d+\.\d+)', out.decode("utf-8"),re.MULTILINE)

def get_routes():
    out = subprocess.check_output(["ip","-4","-o","r","show","dev",iface])
    return re.findall(r'^(\d+\.\d+\.\d+\.\d+/\d+)\s', out.decode("utf-8"),re.MULTILINE)

def get_peers():
    out = subprocess.check_output(["wg","show",iface])
    return re.findall(r'^\s*peer:\s+(\S+)', out.decode("utf-8"),re.MULTILINE)

def clean_peer(exclude):
    for peer in get_peers():
        if peer != exclude:
            print("clean %s" % (peer,))
            subprocess.call(["wg","set",iface,"peer",peer,"remove"])
    return

def clean_ip(exclude):
    for ip in get_ips():
        if ip != exclude:
            print("clean %s" % (ip,))
            subprocess.call(["ip","a","del","%s/32"%(ip),"dev",iface])
    return

def clean_routes(exclude):
    for route in get_routes():
        if not route in exclude:
            print("clean %s" % (route,))
            subprocess.call(["ip","r","del",route,"dev",iface])
    return

def set_ip(ip):
    if subprocess.call(["ip","a","add","%s/32"%(ip),"dev",iface], stderr=subprocess.DEVNULL) == 0:
        print("add %s" % (ip,))
    clean_ip(ip)

def set_routes(routes):
    for route in routes:
        if subprocess.call(["ip","r","add",route,"dev",iface], stderr=subprocess.DEVNULL) == 0:
            print("add %s" % (route,))
    clean_routes(routes)

def set_peer(peer, pubkey):
    subprocess.call(["wg","set",iface,"peer",pubkey,"endpoint",peer,"allowed-ips","0.0.0.0/0","persistent-keepalive","55"])
    clean_peer(pubkey)

while True:
    try:
        r = requests.post(url, data={"hostname":socket.gethostname(), "pubkey":get_pubkey(), "port":60000}, timeout=10)
        j = r.json();
        if j["result"] == "unassigned":
            clean_ip(None)
            clean_peer(None)
            clean_routes([])
        if j["result"] == "ok":
            set_ip(j["ip"])
            set_routes(j["routes"])
            set_peer(j["peer"],j["pubkey"])
    except:
        err = sys.exc_info()
        print(err)
        pass

    time.sleep(5)


