import urllib
import sqlite3
import getpass
import sys
import time
import os
import thread
from pyinotify import *
from crypto import AESCipher
import LocalFileMonitor
import config
#s
class Client:

    def __init__(self):
        self.logged_in = False
        self.lfm = None
        self.lfm = None
        self.CLI()

    def update(self):
        while True:
            n = 6
            time.sleep(n)
            if config.run:
                self.sync(False)
            # get any updated server files every n seconds
            # sdhflksdj;flkj;

    def CLI(self):
        # loggedOutMenu = 'Choose an action by typing the number:\n1: exit\n2: create account\n3: login\n8: help'
        #
        # loggedInMenu = 'Choose an action by typing the number:\n1: exit\n2: create account\n3: login\n' \
        #                '4: turn sync on\n5: turn sync off\n6: change username\n7: change password\n8: help'
        #
        # if self.logged_in:
        #     print loggedInMenu
        # else:
        #     print loggedOutMenu
        #
        command = ''
        #
        # while True:
        #     command = raw_input('CMD: ').split()
        #
        #     if self.logged_in \
        #         and not (command[0] == '1'
        #                  or command[0] == '2'
        #                  or command[0] == '3'
        #                  or command[0] == '4'
        #                  or command[0] == '5'
        #                  or command[0] == '6'
        #                  or command[0] == '7'
        #                  or command[0] == '8'):
        #         print 'invalid command'
        #         continue
        #
        #     elif not self.logged_in \
        #         and not (command[0] == '1'
        #                  or command[0] == '2'
        #                  or command[0] == '3'
        #                  or command[0] == '8'):
        #         print 'invalid command'
        #         continue
        #
        #     else:
        #         # exit
        #         if command[0] == '1':
        #             thread.exit()
        #             exit(0)
        #
        #         # create a new account
        #         if command[0] == '2':
        #             usr = raw_input("Username: ")
        #             pw = 'a'
        #             confirm_pw = 'b'
        #             while pw != confirm_pw:
        #                 pw = raw_input("Password: ")
        #                 confirm_pw = raw_input("Confirm your password: ")
        #                 if pw != confirm_pw:
        #                     print "Passwords do not match."
        #             self.create_account(usr, pw)
        #
        #         # login
        #         if command[0] == '3':
        #             if self.login(): #thread.start_new_thread(self.login(), ()):
        #                 print "Successfully Logged in."
        #                 print loggedInMenu
        #             else:
        #                 print "Incorrect username or password."
        #
        #         # turn sync on
        #         if command[0] == '4':
        #             config.run = True
        #
        #         # turn sync off
        #         if command[0] == '5':
        #             config.run = False
        #
        #         # change username
        #         if command[0] == '6':
        #             success = self.change_username(config.username, config.password)
        #             if success == 'success':
        #                 print 'Username successfully changed.'
        #             else:
        #                 print 'Ya done goofed ;-D'
        #
        #         # change password
        #         if command[0] == '7':
        #             success = self.change_password(config.username, config.password)
        #             if success == 'success':
        #                 print 'Password successfully changed.'
        #             else:
        #                 print 'Ya done goofed ;-D'
        #
        #         # help/print menu
        #         if command[0] == '8':
        #             if self.logged_in:
        #                 print loggedInMenu
        #             else:
        #                 print loggedOutMenu

    def login(self, username, password):
        log = urllib.urlopen(config.url+"/login/" + username + "/" + password).read()
        if log != 'failure':
            config.username = username
            config.password = password
            self.logged_in = True
            config.key = log # log will be the key if login is successful
            self.lfm = thread.start_new_thread(LocalFileMonitor.LocalFileMonitor, ())
            self.sync(True)
            thread.start_new_thread(self.update, ())
            return True
        return False
    '''
    def create_account(self):
        usr = raw_input("Username: ")
        pw = 'a'
        confirm_pw = 'b'
        while pw != confirm_pw:
            pw = raw_input("Password: ")
            confirm_pw = raw_input("Confirm your password: ")
            if pw != confirm_pw:
                print "Passwords do not match."

    '''

    def create_account(self, usr, pw):
        response = urllib.urlopen(config.url+"/account/"+usr+"/"+pw)
        if response.read() != 'created':
            return "Account Exists"
            # self.create_account()
        else:
            return "Account Created."

    def change_password(self, username, password, new_password):
        if urllib.urlopen(config.url + '/' + 'changepw/' + username + '/' + password + '/' + new_password).read() == 'success':
            config.password = new_password
            return 'success'
        else:
            return 'failure'

    def change_username(self, username, password, new_usr):
        if urllib.urlopen(config.url + '/' + 'changeusr/' + username + '/' + password + '/' + new_usr).read() == 'success':
            config.username = new_usr
            return 'success'
        else:
            return 'failure'

    def backup(self):
        return urllib.urlopen(config.url + '/backup/' + config.username + '/' + config.password).read()

    def restore_backup(self):
        return urllib.urlopen(config.url + '/restore_backup/' + config.username + '/' + config.password).read()

    # This method will check the files in a user's onedir folder and compare them to the ones the server has for that
    # user and upload and download the missing files on each end, it is to be called when first logged in, and then
    # periodically to check for updates from other computers
    def sync(self, upload):
        # get the server's list of files for the user (separated by '\0' symbols) to send in one string
        server_files = urllib.urlopen(config.url + '/list/' + config.username + '/' + config.password).read().split('\0')
        server_files.remove('')
        if server_files == ['']:
            server_files = []
        local_files = []
        #(dirpath, dirnames, filenames) for each file and directory
        list_of_directories = os.walk(os.environ['HOME'] + '/onedir') # returns the 3 tuple above
        for files_and_directories in list_of_directories:
            directory = files_and_directories[0]  # stores the path of each directory
            for file in files_and_directories[2]: # for each file in the list of files contained in a directory
                local_files.append(directory + '/' + file)

        #make the server filepaths match the user's
        if len(server_files) > 0: # isn't empty
            for file in server_files:
                server_path = file.split('/')
                server_path.pop(0) # remove ''
                server_path.pop(0) # home
                server_path.pop(0) # user
                server_path.pop(0) # onedir
                server_path.pop(0) # username
                filename = server_path[-1]
                server_path = '/'.join(server_path)
                server_path = os.environ['HOME'] + '/onedir/' + server_path
                # comment
                has = server_path in local_files
                server_newer = False
                valid = urllib.urlopen(config.url+'/validfile'+file).read() == 'valid'
                if has:
                    local_time = float(os.path.getmtime(server_path))
                    server_time = float(urllib.urlopen(config.url+'/lastmodified'+file).read())
                    server_newer = server_time > local_time
                if (valid and not has) or server_newer:
                    server_path = server_path.split('/')
                    filename = server_path.pop()
                    server_path = '/'.join(server_path)
                    if not os.path.exists(server_path):
                        os.makedirs(server_path)
                    os.chdir(server_path)
                    with open(filename, 'w') as dlFile:
                        data = (urllib.urlopen(config.url+'/download/'+config.username+'/'+config.password+file).read())
                        #for line in dlFile.readlines():
                        #print 'encrypted data to decrypt: ' + data
                        dlFile.write(data)
                        #cipher = AESCipher(config.key)
                        #dlFile.write(cipher.decrypt(data))


        #make the user's filepaths match the server's
        if upload:
            if len(local_files) > 0:
                for file in local_files:
                    local_path = file.split('/')
                    local_path.pop(0) # home
                    local_path.pop(0) # user
                    local_path.pop(0) # onedir
                    local_path.pop(0)
                    local_path = '/'.join(local_path)
                    local_path = os.environ['HOME'] + '/onedir/' + config.username + '/' + local_path


                    if os.path.isfile(file) and (local_path not in server_files or float(os.path.getmtime(file)) > float(urllib.urlopen(config.url+'/lastmodified'+local_path).read())):
                        uploadFile(file)

def uploadFile(filePath):
    if config.run:
        with open(filePath, 'rb') as upload:
            urllib.urlopen(config.url+"/upload/"+config.username+"/"+config.password+'/'+"\0" + filePath)
            #data = upload.read()
            #cipher = AESCipher(config.key)
            #encrypted_data = cipher.encrypt(data)

            #for letter in encrypted_data.splitlines():
            for letter in upload.readlines():
                #letter = cipher.encrypt(letter)
                line = []
                for x in letter:
                    line.append(str(ord(x)))
                urllib.urlopen(config.url+"/upload/"+config.username+"/"+config.password+"/" + ' '.join(line) + filePath)



if __name__ == "__main__":
    Client()
