import urllib
import sqlite3
import getpass
#comments lfdjsd;flksdjf
con = sqlite3.connect(":memory:")
c = con.cursor()
c.execute("create table accounts (usr, password)")
class Client:

    def __init__(self):
        #self.url = 'http://172.26.46.188:5000' #home wifi
        self.url = 'http://172.25.42.195:5000' #stacks wifi
        #self.url = 'http://172.25.43.181:5000'
        #self.url = 'http://192.168.1.255:5000' #home Ubuntu server URL
        logged = False
        while not logged:
            self.username = raw_input("Username: ")
            self.password = raw_input("Password: ")
            success = self.login(self.username, self.password)
            if success == 'failure':
                print "Incorrect username or password \nTo quit, enter exit for your username \n To create an account, enter create for your username."
            elif success == 'created':
                print "Account created!"
            else:
                logged = True
        print "Successfully logged in"

        command = ''
        while command != 'exit':
            command = raw_input('CMD: ').split()
            if command[0] == 'upload':
                self.upload(command[1])

    def login(self, username, password):
        if username == "exit":
            exit()
        elif username == 'create':
            usr = raw_input("New Username: ")
            command = "select * from accounts where usr = '%s'" % usr
            c.execute(command)
            value = c.fetchone()
            while value != None:
                print "The specified email address already exists in the database."
                usr = raw_input("New Username: ")
                command = "select * from accounts where usr = '%s'" % usr
                c.execute(command)
                value = c.fetchone()
            pw = getpass.getpass("New Password: ")
            confirm_pw = getpass.getpass("Confirm Password: ")
            while password != confirm_pw:
                print "Passwords do not match."
                password = getpass.getpass("New password: ")
                confirm = getpass.getpass("Confirm password: ")
            c.execute("insert into accounts values (?, ?)", (usr, pw))
            urllib.urlopen(self.url+"/account/" + usr + "/" + pw)
            return 'created'
        return urllib.urlopen(self.url+"/login/" + username + "/" + password)



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