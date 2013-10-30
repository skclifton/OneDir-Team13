import urllib
import sqlite3
import getpass

class Client:

    def __init__(self):
        #self.url = 'http://172.26.46.188:5000' #home wifi
        #self.url = 'http://172.25.42.195:5000' #stacks wifi
        #self.url = 'http://172.25.87.129:5000' #o'hill wifi
        self.url = 'http://10.0.2.15:5000'
        #self.url = 'http://192.168.1.255:5000' #home Ubuntu server URL

        command = ''

        while command != 'exit':
            command = raw_input('CMD: ').split()
            if command[0] == 'upload':
                self.upload(command[1])
            if command[0] == 'create':
                self.create_account()
            if command[0] == 'login':
                if self.login():
                    print "Successfully Logged in."
                else:
                    print "Incorrect username or password."
            if command[0] == 'exit':
                exit()



    def login(self):
        username = raw_input("Username: ")
        password = raw_input("Password: ")
        log = urllib.urlopen(self.url+"/login/" + username + "/" + password).read()
        if log == 'success':
            self.username = username
            self.password = password
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
            print response.read()
            self.create_account()
        else:
            print "Account Created."


    def upload(self, file):
        with open(file, 'rb') as upload:
            print "Uploading", file
            urllib.urlopen(self.url+"/upload/"+self.username+"/"+self.password+"/"+file+"/"+"do not remove this")
            for letter in upload.readlines():
                line = []
                for x in letter:
                    line.append(str(ord(x)))
                #print letter
                urllib.urlopen(self.url+"/upload/"+self.username+"/"+self.password+"/"+file+"/"+' '.join(line))
        print "Done uploading", file


if __name__ == "__main__":
    Client()