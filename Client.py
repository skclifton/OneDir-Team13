import urllib
import sqlite3
import getpass
import LocalFileMonitor
import time
import thread
import os
import sys
from pyinotify import *

path = os.environ['HOME'] + "/onedir"

class Client:

    def __init__(self):
        #self.url = 'http://172.26.46.188:5000' #home wifi
        #self.url = 'http://172.25.42.195:5000' #stacks wifi
        #self.url = 'http://172.25.87.129:5000' #o'hill wifi
        self.url = 'http://10.0.2.15:5000'
        #self.url = 'http://192.168.1.255:5000' #home Ubuntu server URL
        self.logged_in = False
        self.lfm = None
        self.sync = True
        self.username = ''
        self.password = ''
        thread.start_new_thread(self.CLI, ())
        self.main_loop()

    def main_loop(self):
        while True:
            time.sleep(1)
            if self.logged_in and self.sync:
                thread.start_new_thread(self.lfm.update, ())#self.lfm.update()

    def CLI(self):
        command = ''
        while command != 'exit':
            command = raw_input('CMD: ').split()
            if command[0] == 'create':
                #thread.start_new_thread(self.create_account(), ())
                self.create_account()
            if command[0] == 'login':
                if self.login(): #thread.start_new_thread(self.login(), ())
                    print "Successfully Logged in."
                else:
                    print "Incorrect username or password."
            if command[0] == 'sync':
                self.sync = True
            if command[0] == 'unsync':
                self.sync = False
            if command[0] == 'exit':
                sys.exit()




    def login(self):
        username = raw_input("Username: ")
        password = raw_input("Password: ")
        log = urllib.urlopen(self.url+"/login/" + username + "/" + password).read()
        if log == 'success':
            self.username = username
            self.password = password
            self.logged_in = True
            self.lfm = LocalFileMonitor.LocalFileMonitor(username, password)

            return True
        print log
        return False


    def create_account(self):
        usr = raw_input("Username: ")
        pw = 'a'
        confirm_pw = 'b'
        while pw != confirm_pw:
            pw = raw_input("Password: ")
            confirm_pw = raw_input("Confirm your password: ")
            if pw != confirm_pw:
                print "Passwords do not match."

        response = urllib.urlopen(self.url+"/account/"+usr+"/"+pw)
        if response.read() != 'created':
            print "Account Exists"
            print response.read()
            self.create_account()
        else:
            print "Account Created."


if __name__ == "__main__":
    if 'onedir' not in os.listdir(os.environ['HOME']):
        os.mkdir(path)
    Client()