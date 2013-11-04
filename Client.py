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
        #self.url = 'http://10.0.2.15:5000'
        #self.url = 'http://172.25.208.149:5000'
        #self.url = 'http://172.26.46.188:5000' #home wifi
        #self.url = 'http://172.25.42.195:5000' #stacks wifi
        self.url = 'http://172.25.43.190:5000'
        #self.url = 'http://172.25.87.129:5000' #o'hill wifi
        # self.url = 'http://10.0.2.15:5000'
        #self.url = 'http://192.168.1.255:5000' #home Ubuntu server URL
        self.logged_in = False
        self.lfm = None
        # thread.start_new_thread(self.CLI, ())
        self.CLI()
        self.main_loop()


    def main_loop(self):
        while True:
            time.sleep(1)

    def CLI(self):
        loggedOutMenu = 'Choose an action by typing the number:\n1: exit\n2: create account\n3: login\n8: help'

        loggedInMenu = 'Choose an action by typing the number:\n1: exit\n2: create account\n3: login\n' \
                       '4: turn sync on\n5: turn sync off\n6: change username\n7: change password\n8: help'

        if self.logged_in:
            print loggedInMenu
        else:
            print loggedOutMenu

        command = ''

        while True:
            command = raw_input('CMD: ').split()

            if self.logged_in \
                and not (command[0] == '1'
                         or command[0] == '2'
                         or command[0] == '3'
                         or command[0] == '4'
                         or command[0] == '5'
                         or command[0] == '6'
                         or command[0] == '7'
                         or command[0] == '8'):
                print 'invalid command'
                continue

            elif not self.logged_in \
                and not (command[0] == '1'
                         or command[0] == '2'
                         or command[0] == '3'
                         or command[0] == '8'):
                print 'invalid command'
                continue

            else:
                # exit
                if command[0] == '1':
                    thread.exit()
                    exit(0)

                # create a new account
                if command[0] == '2':
                    #thread.start_new_thread(self.create_account(), ())
                    self.create_account()

                # login
                if command[0] == '3':
                    if self.login(): #thread.start_new_thread(self.login(), ()):
                        print "Successfully Logged in."
                        print loggedInMenu
                    else:
                        print "Incorrect username or password."

                # turn sync on
                if command[0] == '4':
                    self.lfm.start_sync()

                # turn sync off
                if command[0] == '5':
                    self.lfm.stop_sync()

                # change username
                if command[0] == '6':
                    print

                # change password
                if command[0] == '7':
                    print

                # help/print menu
                if command[0] == '8':
                    if self.logged_in:
                        print loggedInMenu
                    else:
                        print loggedOutMenu

    def login(self):
        username = raw_input("Username: ")
        password = raw_input("Password: ")
        log = urllib.urlopen(self.url+"/login/" + username + "/" + password).read()
        if log == 'success':
            self.username = username
            self.password = password
            self.logged_in = True
            self.lfm = LocalFileMonitor.LocalFileMonitor(username, password, self.url)
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