#!/usr/bin/env python
#coding:utf-8
# Manage the client connection
#
#
# Mateus-n00b
#
# TODO: Conclude the implementation!
#
from Tkinter import *
from socket import *
from threading import Thread
import irc_cmds
import security
import json,random,os

BUFFER = 1024
gl_port = 2222
AES_Key = str()
AES_IV = str()

nick = "guest-"+hex(random.randint(0,1000))
message = {}
sock = socket(AF_INET,SOCK_STREAM)

class App():
    def __init__(self,master,server_ip):
        global nick
        global message
        port=gl_port

        try:
            sock.connect((server_ip,port))
            print "[!] Establishing a connection... (Running Diffie-Hellman Algorithm)"
            self.authenticate(sock)
            print "[+] Connection established!"
        except Exception as err:
            print "[-] Error {}!".format(err)
            exit(-1)

        message['nick'] = nick  # Your nickname

        self.fontePadrao = ("Arial","10")

        self.container1 = Frame(master)
        self.container1["pady"] = 10
        self.container1.pack()

        self.container2 = Frame(master)
        self.container2["padx"] = 20
        self.container2.pack()

        self.title = Label(self.container1,text="SIRC")
        self.title["font"] = ("Arial","15","bold")
        self.title.pack()

        self.container3 = Frame(master)
        self.container3["padx"] = 10
        self.container3.pack()

        self.messageLabel = Label(self.container3,text="Message: ",font=self.fontePadrao)
        self.messageLabel.pack(side=LEFT)

        self.container4 = Frame(master)
        self.container4["pady"] = 10
        self.container4.pack()

        self.read_message= Entry(self.container3)
        self.read_message["width"] = 30
        self.read_message["font"] = self.fontePadrao
        self.read_message.bind("<Return>",self.send) # Press Enter to send
        self.read_message.pack(side=LEFT)

        self.autenticar = Button(self.container4)
        self.autenticar["text"] = "Send"
        self.autenticar["font"] = ("Calibri","8")
        self.autenticar["command"] = self.send # Press mouse button
        self.autenticar.bind("<Return>",self.send) # Press Enter to send
        self.autenticar.pack()


        self.scrollbar = Scrollbar(self.container2)
        self.scrollbar.pack( side = LEFT, fill=Y )
        self.mylist = Listbox(self.container2, yscrollcommand = self.scrollbar.set )
        self.mylist["width"] = 80
        self.mylist.pack( side = LEFT, fill = BOTH )
        self.scrollbar.config( command = self.mylist.yview )

        r = Thread(group=None,target=self.read)
        r.start()

        self.salut() # Greetings

    def salut(self): # My greetings
        welcome_msg = "\
        \n\
        Welcome to SIRC (Simple IRC)\n\
        This program is currently under development. Therefore, some bugs still remains.\n\
        Any hints mail me (mateus.aluufc@gmail.com)\n\
        For more help just type '@help'\n"
        tmp = ""
        for w in welcome_msg:
            if w != '\n':
                tmp+=w
            else:
                self.mylist.insert(2,tmp)
                tmp = ""


    def send(self,event):
          global message
          global AES_IV
          global AES_IV

          txt = self.read_message.get() # read from the prompt
          if txt: # Add more cmds
              if "@nick:" in txt:
                  message["nick"] = str(txt).split(':')[1]
                  self.mylist.insert(0, message["nick"]+":> nickname updated!") # prints at the prompt

              elif "@help" in txt:
                  self.mylist.insert(0,"'@nick:<new_nick>' to change your nickname") # TODO: Implment the help function
                  self.mylist.insert(0,"'@exit' to exit") # TODO: Implment the help function

              elif "@exit" in txt:
                  os.system("killall python") # Temporary

              else:
                  message['txt'] = txt # To Json
                  self.mylist.insert(0, message["nick"]+":> "+txt) # prints at the prompt
                #   self.mylist.insert(END, message["nick"]+":> "+txt) # prints at end of prompt
                #   self.scrollbar.focus_set() # Interesting
                  msg = security.encrypt_msg(AES_Key,AES_IV,json.dumps(message)) # encrypt_msg
                  sock.send(msg) # sends message
          self.read_message.delete(first=0,last=26) # clear the prompt!!!!

    def read(self):
        global message
        global AES_IV
        global AES_IV

        while 1:
            cipher_msg = sock.recv(1024) # read from buffer
            if not cipher_msg:
                self.mylist.insert(END,"[-] Server seems to be OFFLINE! Exiting...")
                break

            plain_msg = security.decrypt_msg(AES_Key,AES_IV,cipher_msg) # Decrypt msg
            plain_msg = json.loads(plain_msg)
            msg = plain_msg['nick'].encode("utf-8")+':> '+plain_msg['txt'].encode("utf-8")
            self.mylist.insert(0,msg) # print the message

    # TODO: Conclude this function
    def start_connection(self):
        server_ip = Frame(master)
        server_ip["pady"] = 30
        server_ip.pack()

        button_send = Frame(master)
        button_send["pady"] = 20
        button_send.pack()

        insert_ip = Entry(server_ip)
        insert_ip["width"] = 20
        insert_ip["font"] = self.fontePadrao
        insert_ip.pack(side=CENTER)

        messageLabel = Label(insert_ip,text="Server IP: ",font=self.fontePadrao)
        messageLabel.pack(side=LEFT)

        conect = Button(button_send)
        conect["text"] = "Send"
        conect["font"] = ("Calibri","8")
        conect["command"] = self.check_connection
        conect.pack()

    # Authentication
    def authenticate(self,conn):
        global AES_Key
        global AES_IV
        AES_Key,AES_IV = security.diffie_hellman_client(conn) # Generate AES_Key and AES_IV to encrypt the messages
