class Admin:

    def __init__(self):
        self.ADMIN()

    def ADMIN(self):
        menu = 'Choose an action by typing the number:\n1: exit\n2: delete user account\n3: reset user password' \
               '\n4: view sync history\n5: view file information\n6: help'

        print menu

        command = ''

        while True:
            command = raw_input('CMD: ').split()

            if not (command[0] == '1'
                    or command[0] == '2'
                    or command[0] == '3'
                    or command[0] == '4'
                    or command[0] == '5'
                    or command[0] == '6'):
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

                # view sync history
                if command[0] == '4':
                    print

                # view file information
                if command[0] == '5':
                    print

                # help/print menu
                if command[0] == '6':
                    print menu

if __name__ == "__main__":
    Admin()