import urllib


class Admin:
    def __init__(self):
        self.url = 'http://10.0.2.15:5000'
        self.ADMIN()

    def ADMIN(self):
        menu = 'Choose an action by typing the number:\n1: exit\n2: delete user account\n3: reset user password' \
               '\n4: view user information\n5: view sync history\n6: view file information\n7: help'

        print menu

        command = ''

        while True:
            command = raw_input('CMD: ').split()

            if not (command[0] == '1'
                    or command[0] == '2'
                    or command[0] == '3'
                    or command[0] == '4'
                    or command[0] == '5'
                    or command[0] == '6'
                    or command[0] == '7'):
                print 'invalid command'
                continue

            else:
                # exit
                if command[0] == '1':
                    exit(0)

                # delete user account
                if command[0] == '2':
                    print

                 # change user password
                if command[0] == '3':
                    print

                # view user information
                if command[0] == '4':
                    print '---------- START USER INFORMATION ----------'
                    print urllib.urlopen(self.url + "/userinfo").read()
                    print '---------- END USER INFORMATION ----------'

                # view sync history
                if command[0] == '5':
                    print '---------- START SYNC HISTORY ----------'
                    print urllib.urlopen(self.url + "/synchistory").read()
                    print '---------- END SYNC HISTORY ----------'

                # view file information
                if command[0] == '6':
                    print '---------- START FILE INFORMATION ----------'
                    print urllib.urlopen(self.url + "/fileinfo").read()
                    print '---------- START FILE INFORMATION ----------'

                # help/print menu
                if command[0] == '7':
                    print menu

if __name__ == "__main__":
    Admin()