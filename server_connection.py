# Server Side - uses the AES Cryptography to secure the messages
# The key is generated using the Diffie-Hellman Algorithm
#
# Created by Mateus-n00b, September 2017.
#
#
# TODO: Finish the server side and client side
#
#
#
from socket import *
from threading import Thread
import irc_cmds
import security
import json

BUFFER = 1024
gl_port = 2222
AES_Key = str()
AES_IV = str()

sock = socket(AF_INET,SOCK_STREAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

print "\t\tSERVER ONLINE!"
sock.bind(('',gl_port))
sock.listen(5)

def handle_msg(conn,addr):
    global AES_IV
    global AES_Key
    while 1:
            json_msg = conn.recv(BUFFER)

            if not json_msg:
                print "[-] {0} is out!".format(addr[0])
                break

            json_msg = security.decrypt_msg(AES_Key,AES_IV,json_msg) # Decrypt msg
            clean_msg = json.loads(json_msg)
            print clean_msg['nick'].encode("utf-8")+':> '+clean_msg['txt'].encode("utf-8")

def handle_conn():
    while 1:
        try:
            conn, addr = sock.accept()
            print "[!] Connection received from {0}".format(addr)
            print "[!] Establishing a connection... (Running Diffie-Hellman Algorithm)"

            thd = Thread(group=None,target=authenticate,args=(conn,))
            thd.start()

            t = Thread(group=None,target=handle_msg,args=(conn,addr,))
            t.start()
        except Exception as err:
            print "[-] Error on connection! {}".format(err)

# Authentication
def authenticate(conn):
    global AES_Key
    global AES_IV
    AES_Key,AES_IV = security.diffie_hellman_server(conn)
    print "[+] Successful!"

def run():
        handle_conn()

# Local test!
if __name__ == '__main__':
    run()
