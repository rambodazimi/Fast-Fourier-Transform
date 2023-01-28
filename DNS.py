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
    elif (is_A): # type A or standard query (IP address)
        queryType = "A"
        queryNumber = 1 # 0x0001 for a type-A query
    else:
        invalid_type_error()

    # summarize the query to be sent
    summarize(domain_name, ip_address, queryType)

    # build the DNS packet
    # request_packet = packet_builder(domain_name, queryType, queryNumber)

    # send a request to the client after building the DNS packet
    send_request(timeout, max_retries, port, queryNumber, domain_name, ip_address)

    display_output()

def packet_builder(domain_name, queryNumber):
    # build request packets 
    # help from https://stackoverflow.com/questions/24814044/having-trouble-building-a-dns-packet-in-python
    # >H is used we need big Endian for unsigned short and so we need to reverse the bits 
    
    # generate a 16-bit random number for ID for each request
    req_pkt = struct.pack(">H", random.getrandbits(16))

    # Flag
    req_pkt += struct.pack(">H", 0x0100) # 0x0100 = 256 = 0b 0000 0001 0000 0000
    # QR is 0 (query), OPCODE (4 bit) is 0, AA and CC are 0, RD is 1 (recursion), Z (3 bit) is 0, RCODE (4 bit) is 0 (no error in request)

    # QDCOUNT
    req_pkt += struct.pack(">H", 0x0001) # always set to 1

    # ANCOUNT
    req_pkt += struct.pack(">H", 0x0000) # number of Resource Records in the answer section

    # NSCOUNT
    req_pkt += struct.pack(">H", 0x0000) # set to 0 (ignore)

    # ARCOUNT
    req_pkt += struct.pack(">H", 0x0000) # number of Resource Records in the additional records section
    
    # parsing the name server
    # QNAME
    for i in domain_name.split("."): # domain name is a sequence of labels separated by dots
        req_pkt += struct.pack(">B", len(i)) # put the length of each section into question
        for part in i:
            req_pkt+= struct.pack("c", part.encode('utf-8')) # put the characters of each section into question
    req_pkt += struct.pack(">B", 0) # put 0 at the end of QNAME field

    # QTYPE
    req_pkt += struct.pack(">H", queryNumber) # specifying the type of query

    # QCLASS
    req_pkt += struct.pack(">H", 0x0001) # Always 1 representing an Internet address
    return req_pkt

def send_request(timeout, max_retries, port, query_number, domain_name, ip_address):
    finished = False
    for i in range(max_retries): # try sending request max_retries number of times
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # create a client socket object using IPV4 and UDP protocols
        client_socket.settimeout(timeout) # set the timeout for the client socket
        try:
            start_time = time.time()
            # without connecting to any server (TCP), with UDP we can send the request packet to the tuple (ip address, port number)
            client_socket.sendto(packet_builder(domain_name, query_number), (ip_address, port))
            (answer, answer_address) = client_socket.recvfrom(1024) # wait until get an reply from the server
            finished = True
            end_time = time.time()
            time_taken = end_time - start_time # compute the length of time taken to send the request and receive a response from the server
            print(f"Response received after {time_taken} seconds ({i} retries)")
            if (finished): # if a response is received, break from the for loop
                break
        except socket.timeout:
            print(f"ERROR    Time Out Error. You set {timeout} seconds to wait")
            if(i >= max_retries):
                print(f"Maximum number of retries {max_retries} exceeded")

    return answer # return the response received from the server


#same as build packets but unbuild them to be able to decode them later 
def unbuild_packet(result):
    #help from https://www.programcreek.com/python/example/3645/struct.unpack_from
    #the idea is to unpack and increase the offset by 2 since as mentionned in the doc provided 
    #each value is 2 bytes away
    # we only need the firs index of the tuple 

    id_unpack = struct.unpack_from(">H",result)[0]
    flags_unpack = struct.unpack_from(">H",result,2)[0]
    qdCount_unpack = struct.unpack_from(">H",result,4)[0]
    anCount_unpack = struct.unpack_from(">H",result,6)[0]
    anCount_unpack = struct.unpack_from(">H",result,8)[0]
    anCount_unpack = struct.unpack_from(">H",result,10)[0]
    
    list= [id_unpack,flags_unpack,qdCount_unpack,anCount_unpack,anCount_unpack]
    return list


def display_output():
    anCount = unbuild_packet(result).list[3]
    if (anCount):
        print(f"Answer Section ({anCount} records)")
    else:
        print(f"NOTFOUND")

# summarizes the query that is going to be sent
def summarize(domain_name, ip_address, queryType):
    print(f"DnsClient sending request for: {domain_name}")
    print(f"Server: {ip_address}")
    print(f"Request type: {queryType}")


def invalid_type_error():
    print("The query type is invalid!")
    print("Terminating the DNS client application...")
    exit()



if __name__ == "__main__":
    __main__()
