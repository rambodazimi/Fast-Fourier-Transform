from socket import * 
import argparse
import time

#arguments 
default_timeOut = 5
default_maxRetries = 3
default_port = 53

# parse the cmd input 

def __main__ ():
    parse = argparse.ArgumentParser("This will query a DNS server")
    #as mentioned in the doc 
    #time
    parse.add_argument("-t", "--timeout", type=int, default= default_timeOut, help="The time to wait before transmitting an unanswered query")
    #max retries
    parse.add_argument("-r", "--max-retries", type=int, default= default_maxRetries, help="maximum number of times to retransmit an unanswered query")
    #port 
    parse.add_argument("-p", "--port", type=int, default= default_port, help="the UDP port number of the DNS server")
    #domain name
    parse.add_argument("-n", type=str, help="Domain name of the IP address")
    #IP address format of a.b.c.d
    parse.add_argument("-s", type=str, help= "The IPv4 address of the DNS server")

    group = parse.add_mutually_exclusive_group()
    #mail server 
    group.add_argument("-mx", action="store_true", default=False, help="mail query type was sent")
    #name server 
    group.add_argument("-ns", action="store_true", default=False, help="name query type was sent")

