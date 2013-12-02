import getpass
import urllib


class Admin:
    def __init__(self):
        self.url = 'http://10.0.2.15.:5000'
    #     self.ADMIN()
    #
    # def ADMIN(self):
    #     menu = 'Choose an action by typing the number:\n1: exit\n2: delete user account\n3: reset user password' \
    #            '\n4: view user information\n5: view sync history\n6: view file information\n7: help'
    #
    #     print menu
    #
    #     command = ''
    #
    #     while True:
    #         command = raw_input('CMD: ').split()
    #
    #         if not (command[0] == '1'
    #                 or command[0] == '2'
    #                 or command[0] == '3'
    #                 or command[0] == '4'
    #                 or command[0] == '5'
    #                 or command[0] == '6'
    #                 or command[0] == '7'):
    #             print 'invalid command'
    #             continue
    #
    #         else:
    #             # exit
    #             if command[0] == '1':
    #                 exit(0)
    #
    #             # delete user account
    #             if command[0] == '2':
    #                 username = raw_input("Enter username to be deleted: ")
    #                 deletefiles = ''
    #                 while not (deletefiles == 'Y' or deletefiles == 'N'):
    #                     deletefiles = raw_input("Do you want to delete the users files? (Y/N)")
    #                 success = self.delete_account(username, deletefiles)
    #                 if success == 'success':
    #                     print 'User successfully deleted'
    #                 else:
    #                     print 'User does not exist'
    #
    #              # reset user password
    #             if command[0] == '3':
    #                 username = raw_input("Enter username: ")
    #                 new_password = getpass.getpass('Enter new password: ')
    #                 success = self.change_password(username, new_password)
    #                 if success == 'success':
    #                     print 'Password successfully changed.'
    #                 else:
    #                     print 'User does not exist'
    #
    #             # view user information
    #             if command[0] == '4':
    #                 userinfo = urllib.urlopen(self.url + "/userinfo").read().split('\t')
    #                 print "{0:<20} {1:>20}".format("Username", "Password")
    #                 print "-"*41
    #                 i = 0
    #                 j = 1
    #                 while j < len(userinfo):
    #                     print "{0:20} {1:>20}".format(userinfo[i], userinfo[j])
    #                     i += 2
    #                     j += 2
    #
    #             # view sync history
    #             if command[0] == '5':
    #                 print '---------- START SYNC HISTORY ----------'
    #                 print urllib.urlopen(self.url + "/synchistory").read()
    #                 print '---------- END SYNC HISTORY ----------'
    #
    #             # view file information
    #             if command[0] == '6':
    #                 fileinfo = urllib.urlopen(self.url + "/fileinfo").read().split('\t')
    #                 print "{0:<20} {1:^20} {2:>20}".format("User", "File Size", "Number of Files")
    #                 print "-"*62
    #                 i = 0
    #                 j = 1
    #                 k = 2
    #                 while k < len(fileinfo):
    #                     print "{0:20} {1:^20} {2:>20}".format(fileinfo[i], fileinfo[j], fileinfo[k])
    #                     i += 3
    #                     j += 3
    #                     k += 3
    #
    #             # help/print menu
    #             if command[0] == '7':
    #                 print menu

    def change_password(self, username, new_password):
        if urllib.urlopen(self.url + '/' + 'changepwadmin/' + username + '/' + new_password).read() == 'success':
            return 'success'
        return 'failure'

    def delete_account(self, username, deletefiles):
        if urllib.urlopen(self.url + '/' + 'deleteaccount/' + username + '/' + str(deletefiles)).read() == 'success':
            return 'success'
        return 'failure'

if __name__ == "__main__":
    Admin()