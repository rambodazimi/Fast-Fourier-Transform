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
    ip_address = arguments.ip_address
    domain_name = arguments.domain_name
    is_mx = arguments.mx 
    is_ns = arguments.ns
    is_A = (not (is_mx)) and (not (is_ns))

    # just for testing purposes
    print(f"timeout = {timeout}")
    print(f"max retries = {max_retries}")
    print(f"port = {port}")
    print(f"ip address = {ip_address}")
    print(f"domain name = {domain_name}")
    print(f"mx = {is_mx}")
    print(f"ns = {is_ns}")
    print(f"A = {is_A}")

    #from the provided doc 
    if (is_mx):
        queryType = "MX"
        queryNumber = 15
    elif (is_ns):
        queryType = "NS"
        queryNumber = 2
    else:
        queryType = "A"
        queryNumber = 1
    #sending request to the client
    print("DnsClient sending request for:", domain_name)
    print("Server:", ip_address)
    print("Requesttype:", queryType)







if __name__ == "__main__":
    __main__()
