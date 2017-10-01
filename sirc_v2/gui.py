#!/usr/bin/env python
#coding:utf-8
from Tkinter import *

class App():
    def __init__(self,master=None):
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
        self.container4["pady"] = 20
        self.container4.pack()

        self.message = Entry(self.container3)
        self.message["width"] = 30
        self.message["font"] = self.fontePadrao
        self.message.pack(side=LEFT)

        self.autenticar = Button(self.container4)
        self.autenticar["text"] = "Send"
        self.autenticar["font"] = ("Calibri","8")
        self.autenticar["command"] = self.insert_text
        self.autenticar.pack()


        self.scrollbar = Scrollbar(self.container2)
        self.scrollbar.pack( side = LEFT, fill=Y )
        self.mylist = Listbox(self.container2, yscrollcommand = self.scrollbar.set )
        self.mylist["width"] = 80
        self.mylist.pack( side = LEFT, fill = BOTH )
        self.scrollbar.config( command = self.mylist.yview )

    def insert_text(self):
        passw = self.message.get()
        self.mylist.insert(END, passw)
        self.message.delete(first=0,last=26) # apaga os caracteres!!!!

root = Tk()
App(root)
root.mainloop()
