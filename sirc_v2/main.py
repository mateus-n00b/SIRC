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
from Tkinter import *
import server_connection
import client_connection
import getopt,sys

# Men at work
# For a simple test, run in a terminal:
 # $ python server_connection.py
# Open other terminal and run:
 # $ python client_connection.py

if len(sys.argv) < 2:
        print "Usage: {0} -c|--client <server_ip> (play as a client) or -s (play as a server)\n\
       {0} -c 127.0.0.1 - connect to server '127.0.0.1'".format(sys.argv[0])
        exit(-1)

opts,args =  getopt.getopt(sys.argv[1:],"hsc:",["client,help"])
for o,a in opts:
    if o in ("-h","--help"):
        print "Usage: {0} -c (play as a client) or -s (play as a server)".format(sys.argv[0])
        exit(-1)
    elif o in ("-s", "--server"):
        server_connection.run()

    elif o in ("-c","--client"):
        root = Tk()
        client_connection.App(master=root,server_ip=a)
        root.mainloop()

    else:
        print "Invalid option! Try -h."
        exit(-1)
