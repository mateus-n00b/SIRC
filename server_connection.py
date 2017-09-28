# Server Side - uses the AES Cryptography to secure the messages
# The key is generated using the Diffie-Hellman Algorithm
#
# Created by Mateus-n00b, September 2017.
#
# Version: 1.0
# TODO:
#       Implement the server-client key exchange, for warning messages.
#       The IRC cmds.
#
#
from socket import *
from threading import Thread
import irc_cmds
import security
import json

BUFFER = 1024
gl_port = 2222
CONNECTIONS = list() # Holds the current connections
KEYs_IVs = dict() # Holds the KEY and IV linked to a connection (e.g KEYs_IVs[user1] == ('password','myIV'))

sock = socket(AF_INET,SOCK_STREAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

def handle_msg(conn,port):
    global CONNECTIONS
    global KEYs_IVs

    while 1:
            json_msg = conn.recv(BUFFER)

            if not json_msg:
                print "[-] {0} is out!".format(addr[0])
                break

            for obj,p in CONNECTIONS:
                if obj != conn:
                    json_msg = security.decrypt_msg(KEYs_IVs[port][0],KEYs_IVs[port][1],json_msg) # Decrypt msg with my KEY
                    cipher_txt = security.encrypt_msg(KEYs_IVs[p][0],KEYs_IVs[p][1],json_msg) # Encrypt the message with the key of the endpoint
                    try:
                        obj.send(cipher_txt) # send the message to the endpoint
                    except:
                        CONNECTIONS.remove((obj,p))
                    # print clean_msg['nick'].encode("utf-8")+':> '+clean_msg['txt'].encode("utf-8")


def handle_conn(sock):
    global CONNECTIONS
    while 1:
        try:
            conn, addr = sock.accept()
            print "[!] Connection received from {0}".format(addr)
            print "[!] Securing the connection... (Running Diffie-Hellman Algorithm)"

            # I'm using the port number as an ID for the connection to retrieve its key and iv
            thd = Thread(group=None,target=authenticate,args=(conn,addr[1],))
            thd.start()

            if conn not in CONNECTIONS:
                CONNECTIONS.append((conn,addr[1]))

            t = Thread(group=None,target=handle_msg,args=(conn,addr[1],))
            t.start()

        except Exception as err:
            print "[-] Error on connection! Error:\n{}".format(err)

# Authentication
def authenticate(conn,port):
    global KEYs_IVs
    AES_Key = str()
    AES_IV = str()
    AES_Key,AES_IV = security.diffie_hellman_server(conn)
    KEYs_IVs[port] = (AES_Key,AES_IV)
    print "[+] Successful!"

def run():
        print "\t\tSERVER ONLINE!"
        sock.bind(('',gl_port))
        sock.listen(5)
        handle_conn(sock)

# Local test!
if __name__ == '__main__':
    run()
