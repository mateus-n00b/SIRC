# created by Mateus-n00b
#
# 01/04/2018 - Salvador, Brazil
#
# TODO: Add security module
#
from Tkinter import *
from threading import Thread
import requests
import json,random,os,time


class App:
    def __init__(self,master,url):
        self.nick = "guest-"+hex(random.randint(0,1000)) # random nickname
        self.message = dict() # message structure

        self.url = url # room ID
        self.r = requests # requests module


        # Testing connection
        if not self.test_conn():
            print "Error on connecting to {}".format(self.url)
            exit(-1)

        self.message['nick'] = self.nick  # Your nickname

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
        Welcome to SIRC (Simple IRCv3)\n\
        Program currently under development. Some bugs may appears.\n\
        Hints? Mail me (mateus.aluufc@gmail.com)\n\
        For more help just type '@help'\n"
        tmp = ""
        for w in welcome_msg:
            if w != '\n':
                tmp+=w
            else:
                self.mylist.insert(3,tmp)
                tmp = ""


    def test_conn(self):
        status = self.r.get(self.url)
        if int(status.status_code) != 200:
            return False
        return True


    def send(self,event):
          txt = self.read_message.get() # read from the prompt
          if txt: # Add more cmds
              if "@help" in txt:
                  self.mylist.insert(0,"Type '@nick=<new_nick>' to change your nickname") # TODO: Implment the help function
                  self.mylist.insert(0,"'@exit' to exit") # TODO: Implment the help function

              elif "@exit" in txt:
                  os.system("killall python") # Temporary

              elif "@nick" in txt:
                  try:
                      self.nick = str(txt).split('=')[1]
                      self.message["nick"] = self.nick
                      self.mylist.insert(0, self.message["nick"]+":> nickname updated!") # prints at the prompt
                  except Exception as err:
                        self.mylist.insert(0, "Invalid command! Try '@help'") # prints at the prompt

              else:
                  self.message['txt'] = txt # To Json
                  self.message['status'] = False
                  self.mylist.insert(0, self.message["nick"]+":> "+txt) # prints at the prompt
                  self.r.post(self.url,data={"text":json.dumps(self.message)}) # sends self.message
          self.read_message.delete(first=0,last=26) # clear the prompt!!!!

    def read(self):
        while 1:
            cipher_msg = self.r.get(url=self.url) # read from buffer
            plain_msg = cipher_msg.content.split('text">')[1].split('</textarea>')[0] # Armengss

            if not plain_msg:
                self.message['txt'] = "Hi!"
                self.message['status'] = False
                self.r.post(self.url,data={"text":json.dumps(self.message)}) # sends self.message

            else:
                try:
                    to_json = json.loads(str(plain_msg))
                    if not bool(to_json['status']) and to_json['nick'] != self.nick: # Msg already readed?
                        msg = to_json['nick'].encode("utf-8")+':> '+to_json['txt'].encode("utf-8")
                        self.mylist.insert(0,msg) # print the self.message
                        self.message['status'] = True
                        # NOTE: The line bellow deletes the self.message after read it (wrong way!!!!)
                        self.r.post(self.url,data={"text":json.dumps(self.message)}) # TODO: Fix this part. You'll need to treat self.messages lifetime
                except Exception as err:
                    print "[-] {}".format(err)
                    time.sleep(0.3)
