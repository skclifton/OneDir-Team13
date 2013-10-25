import urllib
#comments lfdjsd;flksdjf
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
            pw = raw_input("New Password: ")
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