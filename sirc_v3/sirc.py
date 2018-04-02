#!/usr/bin/env python
# created by Mateus-n00b
#
# SIRC v3.0
#   NOTE: Now SIRC works by using dontpad as a server to create chat rooms.
#         Thus, users can communicate each others globally.
#
# 01/04/2018 - Salvador, Brazil
#
# TODO: Add security module.
# NOTE: messages are sent in plain text

from Tkinter import *
import client_connection
import getopt,sys

if len(sys.argv) < 2:
        print "Usage: {0} -c|--connect  (connect to/create chat room)\n\
       {0} -c room1 - connect to/create room 'room1'".format(sys.argv[0])
        exit(-1)

opts,args =  getopt.getopt(sys.argv[1:],"hc:",["connect,help"])
for o,a in opts:
    if o in ("-h","--help"):
        print "Usage: {0} -c|--connect  (connect to/create chat room)\n\
       {0} -c room1 - connect to/create room 'room1'".format(sys.argv[0])
        exit(-1)

    elif o in ("-c","--client"):
        root = Tk()
        url = "http://dontpad.com/{}".format(a) # Using dontpad as my infrastructure
        client_connection.App(master=root,url=url)
        root.mainloop()

    else:
        print "Invalid option! Try -h."
        exit(-1)
