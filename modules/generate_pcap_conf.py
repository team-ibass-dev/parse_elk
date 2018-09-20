# -*- coding:UTF-8 -*-

import os
import binascii
import socket
import dpkt
"""dpkt est un module qui permet de manipuler les paquet issus d'un réseau"""


def chFormatMAC(mac):
    """Changer une adresse MAC binaire en adresse MAC au format ASCII"""

    macAscii = binascii.b2a_hex(mac)
    macAscii = macAscii.decode()
    result = ':'.join(macAscii[i:i + 2] for i in range(0, 12, 2))
    return result


def chFormatIP(ip, ipType):
    """Changer une adresse IP binaire en adresse ip au format ASCII"""
    if ipType == 'IP':
        result = socket.inet_ntoa(ip)
    else:
        result = socket.inet_ntop(socket.AF_INET6, ip)

    return result
def generate(path):
    k = 1
    print(path)
    chaine = '''sourceMAC,destinationMAC,sourceIP,destinationIP,sourcePort,destinationPort,prot,ipType'''
    for ts, pkt in dpkt.pcap.Reader(open(path, 'rb')):

        eth = dpkt.ethernet.Ethernet(pkt)
        # print(macAdress(eth.dst))
        ip = eth.data
        try:
            ipType = str(ip.get_proto.__self__.__name__)
        except Exception as e:
            print("Nous ne prenons pas en compte ce paquet")
        else:
            # ip.src est l'adresse ipv4 source du paquet
            # ip.dst est l'adresse ipv4 de destination du paquet
            # len(tcp.data)  la longueur des donnees de chaque paquet
            # tcp.sport le port source de l'entete
            # tcp.dport le port destination

            if ip.p == dpkt.ip.IP_PROTO_TCP:
                prot = "TCP"
            if ip.p == dpkt.ip.IP_PROTO_UDP:
                prot = "UDP"
            if ip.p == dpkt.ip.IP_PROTO_ICMP:
                prot = "ICMP"
            if ip.p == dpkt.ip.IP_PROTO_ICMP6:
                prot = "ICMPv6"

            sourceMAC = str(chFormatMAC(eth.src))
            destinationMAC = str(chFormatMAC(eth.dst))
            sourceIP = str(chFormatIP(ip.src, ipType))
            destinationIP = str(chFormatIP(ip.dst, ipType))
            sourcePort = " - "
            destinationPort = " - "

            data1 = ip.data

            # print("",ip.id, " -- ", socket.inet_ntoa(ip.src)," -- ",socket.inet_ntoa(ip.dst)," -- ",tcp.sport," -- ",tcp.dport," -- ",len(tcp.data),"-- TCP")
            if (prot != 'ICMP') & (prot != 'ICMPv6'):
                sourcePort = data1.sport
                destinationPort = data1.dport

                if data1.dport == 80 and len(data1.data) > 0:
                    http = dpkt.http.Request(data1.data)
                    # saveElascticsearch(data,k)
                    # print(" -- ", http.uri, " -- ", http.method)
                    # print("",ip.id, " -- ", socket.inet_ntoa(ip.src)," -- ",socket.inet_ntoa(ip.dst)," -- ",udp.sport," -- ",udp.dport," -- ",len(udp.data),"-- UDP")

            chaine = chaine + '''\n'''+sourceMAC+''','''+destinationMAC+''','''''+sourceIP+''','''+destinationIP+''','''+str(sourcePort)+''','''+str(destinationPort)+''','''+prot+''','''+ipType
            k = k + 1
    return chaine

    # socket.inet_ntoa decode adresse ip
    # binascii.b2a_hex decode adresse mac
