#!/usr/bin/env python
# Simple IRC
# Created by Mateus-n00b, September - 2017 (BR)
# Version 1.0
# NOTE:
#       Current features:
#                       - keys-exchange using Diffie-Hellman
#                       - Messages encrypted using AES
#                       - Using Threads to send and read Messages
#
# TODO: A lot of things
#      - implements the server side
#      - control the IVs and KEYs of each session (every key used are different)
#      - Treat the errors and Exceptions
#
# This project is still under development, therefore, there are a lot of work to be done.
#
# License: GPLv3
#

import server_connection
import client_connection
import getopt,sys

# Men at work
# For a simple test, run in a terminal:
 # $ python server_connection.py
# Open other terminal and run:
 # $ python client_connection.py

if len(sys.argv) < 2:
        print "Usage: {0} -t <ServerIP> or -s (play as a server)\n\
       {0} -t 127.0.0.1      Connect to a server\n".format(sys.argv[0])
        exit(-1)

opts,args =  getopt.getopt(sys.argv[1:],"hst:",["target,help"])
for o,a in opts:
    if o in ("-h","--help"):
        print "Usage: {0} -t <ServerIP> or -s (play as a server)\n\
       {0} -t 127.0.0.1      Connect to a server\n".format(sys.argv[0])
        exit(-1)
    elif o in ("-s", "--server"):
        # t = Thread(None,serverSide,None)
        # t.start()
        # Inicia o servidor
        server_connection.run()
    elif o in ("-t","--target"):
        SERVER = a
        # Inicia o cliente
        client_connection.run(a)
    else:
        print "Invalid option! Try -h."
        exit(-1)
