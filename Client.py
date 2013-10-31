import urllib
import sqlite3
import getpass
import sys
import LocalFileMonitor
import time
import thread

class Client:

    def __init__(self):
        #self.url = 'http://10.0.2.15:5000'
        self.url = 'http://172.25.208.149:5000'
        #self.url = 'http://172.26.46.188:5000' #home wifi
        #self.url = 'http://172.25.42.195:5000' #stacks wifi
        #self.url = 'http://172.25.87.129:5000' #o'hill wifi
        # self.url = 'http://10.0.2.15:5000'
        #self.url = 'http://192.168.1.255:5000' #home Ubuntu server URL
        self.logged_in = False
        self.lfm = None
        thread.start_new_thread(self.CLI, ())
        self.main_loop()

    def main_loop(self):
        while True:
            time.sleep(1)

    def CLI(self):
        command = ''
        while command != 'exit':

            if self.logged_in:
                thread.start_new_thread(self.lfm.update, ())#self.lfm.update()

            command = raw_input('CMD: ').split()
            if command[0] == 'create':
                #thread.start_new_thread(self.create_account(), ())
                self.create_account()
            if command[0] == 'login':
                if self.login(): #thread.start_new_thread(self.login(), ()):
                    print "Successfully Logged in."
                else:
                    print "Incorrect username or password."
            if command[0] == 'exit':
                exit(0)


    def login(self):
        username = raw_input("Username: ")
        password = raw_input("Password: ")
        log = urllib.urlopen(self.url+"/login/" + username + "/" + password).read()
        if log == 'success':
            self.username = username
            self.password = password

            self.lfm = LocalFileMonitor.LocalFileMonitor(username, password)

            return True

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
            self.create_account()
        else:
            print "Account Created."


if __name__ == "__main__":
    Client()