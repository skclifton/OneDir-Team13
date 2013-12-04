import getpass
import urllib
import config
import sys


class Admin:
    def __init__(self):
        pass

    def change_password(self, username, new_password):
        if urllib.urlopen(config.url + '/' + 'changepwadmin/' + username + '/' + new_password).read() == 'success':
            return 'success'
        return 'failure'

    def delete_account(self, username, deletefiles):
        if urllib.urlopen(config.url + '/' + 'deleteaccount/' + username + '/' + str(deletefiles)).read() == 'success':
            return 'success'
        return 'failure'

if __name__ == "__main__":
    config.url = sys.argv[1]
    Admin()