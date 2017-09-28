# Manage the client connection
#
#
# Mateus-n00b
#
# TODO: Conclude the implementation!
#
from socket import *
from threading import Thread
import irc_cmds
import security
import json,random

BUFFER = 1024
gl_port = 2222
AES_Key = str()
AES_IV = str()

nick = "guest-"+hex(random.randint(0,1000))
message = {}
sock = socket(AF_INET,SOCK_STREAM)

def send():
    while 1:
          txt = raw_input("{0}>: ".format(nick))
          message['txt'] = txt
          if txt:
              msg = security.encrypt_msg(AES_Key,AES_IV,json.dumps(message))
              sock.send(msg)

def read():
    while 1:
        cipher_msg = sock.recv(1024) # read from buffer
        if not msg:
            print "[-] Server seems to be OFFLINE! Exiting..."
            break

        plain_msg = security.decrypt_msg(AES_Key,AES_IV,cipher_msg) # Decrypt msg
        plain_msg = json.loads(plain_msg)
        print plain_msg['nick'].encode("utf-8")+':> '+plain_msg['txt'].encode("utf-8") # print the message

# Authentication
def authenticate(conn):
    global AES_Key
    global AES_IV
    AES_Key,AES_IV = security.diffie_hellman_client(conn) # Generate AES_Key and AES_IV to encrypt the messages


def run(server_ip,port=gl_port): # start a new connection (set the server_ip and port)
    global nick
    global message

    tmp = raw_input("Your nickname: ")
    if tmp:
        nick = tmp

    try:
        sock.connect((server_ip,port))
        print "[!] Establishing a connection... (Running Diffie-Hellman Algorithm)"
        authenticate(sock)
        print "[+] Connection established!"
    except:
        print "[-] Error to connect with {}!".format(server_ip)
        exit(-1)

    message['nick'] = nick  # Your nickname

    r = Thread(group=None,target=read)
    r.start()

    s = Thread(group=None,target=send)
    s.start()

# For debug reasons!
def main():
    run("localhost",gl_port)


if __name__ == '__main__':
    main()
