# DNS Client Application
# Authors:
# Saghar Sahebi
# Rambod Azimi
# ECSE 316 - Assignment 1 - Winter 2023
# Group 39

"""
This application is implementing a domain name system (DNS) client using sockets in Python
It sends a query to the server for the given domain name using a UDP socket protocol and interprets the response to the terminal
The DNS client should send queries for A (IP address), NS (name server), and MX (mail server) records
The syntax for running the app is the following:
python3 DnsClient [-t timeout] [-r max-retries] [-p port] [-mx|-ns] @server name
"""

import socket
import argparse # to run a Python script with multiple arguments with cmd
import time
import struct
import random

# default arguments 
default_timeOut = 5 # gives how long to wait before retransmitting an unanswered query
default_maxRetries = 3 # max number of times to retransmit an uanswered query before giving up 
default_port = 53 # UPD port number

def __main__ ():
    parse = argparse.ArgumentParser("This will query a DNS server", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # time with the default value of 5 sec
    parse.add_argument("-t", "--timeout", type=int, default= default_timeOut, help="The time to wait before transmitting an unanswered query")

    # max retries with the default value of 3
    parse.add_argument("-r", "--maxretries", type=int, default= default_maxRetries, help="Maximum number of times to retransmit an unanswered query")

    # port with the default value of 53
    parse.add_argument("-p", "--port", type=int, default= default_port, help="The UDP port number of the DNS server")

    # IPv4 address of the DNS server in a.b.c.d format (required)
    parse.add_argument(dest="ip_address", type=str, help= "The IPv4 address of the DNS server")

    # domain name (required)
    parse.add_argument(dest="domain_name", type=str, help="Domain name of the IP address")

    group = parse.add_mutually_exclusive_group() # so that the user can't select both types -mx and -ns together

    # mail server
    group.add_argument("-mx", action="store_true", default=False, help="Mail server query")

    # name server
    group.add_argument("-ns", action="store_true", default=False, help="Name server query type")

    # put all the parser arguments into a variable
    arguments = parse.parse_args()

    # storing each argument to its corresponding variable
    timeout = arguments.timeout
    max_retries = arguments.maxretries
    port = arguments.port
    ip_address = arguments.ip_address[1:] # to remove the first letter (@) of the ip_address typed by the user
    domain_name = arguments.domain_name
    is_mx = arguments.mx 
    is_ns = arguments.ns
    is_A = (not (is_mx)) and (not (is_ns))

    # from the provided doc 
    if (is_mx): # mail server query
        queryType = "MX"
        queryNumber = 15 # 0x000f for a type-MX query
    elif (is_ns): # name server query
        queryType = "NS"
        queryNumber = 2 # 0x0002 for a type-NS query
    else: # type A or standard query (IP address)
        queryType = "A"
        queryNumber = 1 # 0x0001 for a type-A query

def packet_builder(domain_name, queryType):
    #build request packets 
    #help from https://stackoverflow.com/questions/24814044/having-trouble-building-a-dns-packet-in-python
    #>H is used we need big Endian for unsigned short and so we need to reverse the bits 
    
    #as suggested randome numbers will be used each time for the ID
    #ID
    req_pkt = struct.pack(">H", random.getrandbits(16))
    #Flag
    req_pkt += struct.pack(">H", 0x100)
    #QDCOUNT
    req_pkt += struct.pack(">H", 0x0001)
    #ANCOUNT
    req_pkt += struct.pack(">H", 0x0000)
    #NSCOUNT
    req_pkt += struct.pack(">H", 0x0000)
    #ARCOUNT
    req_pkt += struct.pack(">H", 0x0000)
    
    #parsing the name server
    for i in domain_name.split("."):
        req_pkt += struct.pack(">B", len(i))
        for part in i:
            req_pkt+= struct.pack("c", part.encode('utf-8'))
    #QNAME
    req_pkt += struct.pack(">B", 0x0000)
    #QTYPE
    req_pkt += struct.pack(">H", queryType)
    #QCLASS
    req_pkt += struct.pack(">H", 0x0001)
    # summarize the query to be sent
    
    summarize(domain_name, ip_address, queryType)

    # sending request to the client
    send_request(timeout, max_retries, port, queryNumber, domain_name, ip_address)
    display_output()


def send_request(timeout, max_retries, port, query_number, domain_name, ip_address):
    pass


def display_output():
    pass


def summarize(domain_name, ip_address, queryType):
    print(f"DnsClient sending request for: {domain_name}")
    print(f"Server: {ip_address}")
    print(f"Request type: {queryType}")






if __name__ == "__main__":
    __main__()
