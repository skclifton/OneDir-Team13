import urllib
import sqlite3
import getpass
import sys
import LocalFileMonitor
import time
import os
import thread


class Client:

    def __init__(self):

        self.url = 'http://172.25.42.25:5000'
        self.logged_in = False
        self.lfm = None
        self.CLI()

    def update(self):
        while True:
            n = 6
            time.sleep(n)
            self.sync(False)
            # get any updated server files every n seconds
            # sdhflksdj;flkj;

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
            self.lfm = thread.start_new_thread(LocalFileMonitor.LocalFileMonitor, (username, password, self.url))
            self.sync(True)
            thread.start_new_thread(self.update, ())
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

    # This method will check the files in a user's onedir folder and compare them to the ones the server has for that
    # user and upload and download the missing files on each end, it is to be called when first logged in, and then
    # periodically to check for updates from other computers
    def sync(self, upload):
        # get the server's list of files for the user (separated by '\0' symbols) to send in one string
        server_files = urllib.urlopen(self.url + '/list/' + self.username + '/' + self.password).read().split('\0')
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
        #print 'local files: ' + str(local_files)

        #make the server filepaths match the user's
        #print 'server files: ' + str(server_files) + 'size: ' + str(len(server_files))
        if len(server_files) > 0: # isn't empty
            for file in server_files:
                server_path = file.split('/')
                #print 'server path' + str(server_path)
                server_path.pop(0) # remove ''
                server_path.pop(0) # home
                server_path.pop(0) # user
                server_path.pop(0) # onedir
                server_path.pop(0) # username
                filename = server_path[-1]
                server_path = '/'.join(server_path)
                server_path = os.environ['HOME'] + '/onedir/' + server_path
                #print 'file on server: ' + file
                # comment
                has = server_path in local_files
                server_newer = False
                valid = urllib.urlopen(self.url+'/validfile'+file).read() == 'valid'
                if has:
                    local_time = float(os.path.getmtime(server_path))
                    server_time = float(urllib.urlopen(self.url+'/lastmodified'+file).read())
                    server_newer = server_time < local_time
                print 'last modified on server: ' + str(server_time) + ', last modified on client: ' + str(local_time)
                print 'file: ' + file
                print 'valid: ' + str(valid) + ' has: ' + str(has) + ' server_newer: ' + str(server_newer)
                print 'time different: ' + str(server_time - local_time)
                if (valid and not has) or server_newer:
                    server_path = server_path.split('/')
                    filename = server_path.pop()
                    server_path = '/'.join(server_path)
                    if not os.path.exists(server_path):
                        os.makedirs(server_path)
                    os.chdir(server_path)
                    with open(filename, 'w') as dlFile:
                        data = (urllib.urlopen(self.url+'/download/'+self.username+'/'+self.password+file).read())
                        print data
                        dlFile.write(data)


        #make the user's filepaths match the server's
        if upload:
            print 'First time upload'
            if len(local_files) > 0:
                for file in local_files:
                    local_path = file.split('/')
                    local_path.pop(0) # home
                    local_path.pop(0) # user
                    local_path.pop(0) # onedir
                    local_path.pop(0)
                    local_path = '/'.join(local_path)
                    local_path = os.environ['HOME'] + '/onedir/' + self.username + '/' + local_path
                    # print 'path on server: ' + local_path

                    if os.path.isfile(file) and (local_path not in server_files or float(os.path.getmtime(file)) > float(urllib.urlopen(self.url+'/lastmodified'+local_path).read())):
                        self.uploadFile(file)

    def uploadFile(self, filePath):
        with open(filePath, 'rb') as upload:
            print "Uploading", filePath
            urllib.urlopen(self.url+"/upload/"+self.username+"/"+self.password+'/'+"\0" + filePath)
            for letter in upload.readlines():
                line = []
                for x in letter:
                    line.append(str(ord(x)))
                urllib.urlopen(self.url+"/upload/"+self.username+"/"+self.password+"/" + ' '.join(line) + filePath)
        print "Done uploading", filePath



if __name__ == "__main__":
    if 'onedir' not in os.listdir(os.environ['HOME']):
        os.mkdir(os.environ['HOME'] + '/ondedir')
    Client()
    Client()