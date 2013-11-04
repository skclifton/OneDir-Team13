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
        #self.url = 'http://172.25.43.190:5000'
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
                    success = self.change_username(self.username, self.password)
                    if success == 'success':
                        print 'Username successfully changed.'
                    else:
                        print 'Ya done goofed ;-D'

                # change password
                if command[0] == '7':
                    success = self.change_password(self.username, self.password)
                    if success == 'success':
                        print 'Password successfully changed.'
                    else:
                        print 'Ya done goofed ;-D'

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

    def change_password(self, username, password2):
        confirm_pw = 'z'
        new_password = getpass.getpass('Enter your new password: ')
        while not new_password == confirm_pw:
            confirm_pw = getpass.getpass('Enter your new password: ')

        if urllib.urlopen(self.url + '/' + 'changepw/' + username + '/' + password2 + '/' + new_password).read() == 'success':
            self.password = new_password
            self.lfm.set_password(new_password)

            return 'success'
        else:
            return 'failure'

    def change_username(self, username2, password):
        confirm_usr = 'z'
        new_usr = raw_input('Enter your new username: ')
        while not new_usr == confirm_usr:
            confirm_usr = raw_input('Enter your new username: ')

        if urllib.urlopen(self.url + '/' + 'changeusr/' + username2 + '/' + password + '/' + new_usr).read() == 'success':
            self.username = new_usr
            self.lfm.set_username(new_usr)

            return 'success'
        else:
            return 'failure'

if __name__ == "__main__":
    Client()