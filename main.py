#!/usr/bin/env python
# Simple IRC
# Created by Mateus-n00b, September - 2017 (BR)
#
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

# Men at work
# For a simple test, run in a terminal:
 # $ python server_connection.py
# Open other terminal and run:
 # $ python client_connection.py
