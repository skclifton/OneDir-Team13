__author__ = 'student'
from ttk import Style
import tkMessageBox as box
import LocalFileMonitor
import Server
import Admin
import Client
import urllib
import config

from Tkinter import *

gray = "#626864"
blue = "#639793"

class LoggedOut(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("OneDir")
        self.style = Style()
        Style().configure("TButton", padding=(0, 5, 0, 5))
        self.style.theme_use("default")
        self.centerWindow()
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(0, pad=5)
        self.columnconfigure(1, pad=5)
        self.columnconfigure(2, pad=5)

        self.rowconfigure(0, pad=20)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)
        self.rowconfigure(5, pad=3)

        onedirLabel = Label(self, text="OneDir Admin", font='25')
        onedirLabel.grid(row=0, column=0, rowspan=2)


        def other_del_acct(usr):
            if not (usr == ''):
                adm = Admin.Admin()
                response = adm.delete_account(usr, deletefiles = True)
                if response == 'failure':
                    del_acct_error(self)
                else:
                    del_acct_success(self)
            else:
                error(self)


        def del_acct():
            root = Tk()
            root.wm_title("Delete Account")
            root.option_add('*foreground', gray)
            root.option_add('*Button*background', 'white')
            root.option_add('*Entry*background', 'white')
            usernameLabel = Label(root, text="Username:")
            usernameLabel.grid(row=2, column=0, pady=5, padx=5)
            usrTf = Entry(root)
            usrTf.grid(row=2, column=1, columnspan=2, padx=5, sticky=E + W)
            b = Button(root, text = "Change Password", command = lambda: other_del_acct(usrTf.get()))
            b.grid(row = 3, column = 1)
            root.mainloop()

        def other_reset_pw(usr, pw):
            if not (usr == '' or pw ==''):
                adm = Admin.Admin()
                response = adm.change_password(usr, pw)
                if response == 'failure':
                    change_pw_error(self)
                else:
                    change_pw_success(self)
            else:
                error_2(self)


        def reset_pw():
            root = Tk()
            root.wm_title("Change Password")
            root.option_add('*foreground', gray)
            root.option_add('*Button*background', 'white')
            root.option_add('*Entry*background', 'white')
            usernameLabel = Label(root, text="Username:")
            usernameLabel.grid(row=2, column=0, pady=5, padx=5)
            usrTf = Entry(root)
            usrTf.grid(row=2, column=1, columnspan=2, padx=5, sticky=E + W)
            passwordLabel = Label(root, text="Password:")
            passwordLabel.grid(row=3, column=0, pady=5, padx=5)
            pwTf = Entry(root, show="*")
            pwTf.grid(row=3, column=1, columnspan=2, padx=5, sticky=E + W)
            b = Button(root, text = "Change Password", command = lambda: other_reset_pw(usrTf.get(), pwTf.get()))
            b.grid(row = 4, column = 1)
            root.mainloop()


        def view_user_info():
            root = Tk()
            root.wm_title("View User Info")
            userinfo = urllib.urlopen(config.url + "/userinfo").read().split('\t')
            #print "{0:<20} {1:>20}".format("Username", "Password")
            a = Label(root, text = "{0:<20} {1:>20}".format("Username", "Password"))
            a.pack()
            #print "-"*41
            b = Label(root, text = "-"*41)
            b.pack()
            i = 0
            j = 1
            while j < len(userinfo):
                #print "{0:20} {1:>20}".format(userinfo[i], userinfo[j])
                c = Label(root, text = "{0:20} {1:>20}".format(userinfo[i], userinfo[j]))
                i += 2
                j += 2

        def view_sync_info():
            root = Tk()
            root.wm_title("View Sync Info")
            root.option_add('*background', blue)
            root.option_add('*foreground', 'black')
            root.option_add('*Button*background', 'white')
            root.option_add('*Entry*background', 'white')
            usernameLabel = Label(root, text="Username:")
            b = Label(root, text = urllib.urlopen(config.url + "/synchistory").read())
            b.pack()
            root.mainloop()

        def view_file_info():
            root = Tk()
            root.wm_title("View File Info")
            fileinfo = urllib.urlopen(config.url + "/fileinfo").read().split('\t')
            #print "{0:<20} {1:^20} {2:>20}".format("User", "File Size", "Number of Files")
            a = Label(root, text = "{0:<20} {1:^20} {2:>20}".format("User", "File Size", "Number of Files"))
            a.pack()
            #print "-"*62
            b = Label(root, text = "-"*62)
            b.pack()
            i = 0
            j = 1
            k = 2
            while k < len(fileinfo):
                #print "{0:20} {1:^20} {2:>20}".format(fileinfo[i], fileinfo[j], fileinfo[k])
                c = Label(root, text = "{0:20} {1:^20} {2:>20}".format(fileinfo[i], fileinfo[j], fileinfo[k]))
                c.pack()
                i += 3
                j += 3
                k += 3
            root.mainloop()


        def error(self):
            box.showerror("", "Enter a username")

        def error_2(self):
            box.showerror("", "Enter a username and a new password")

        def del_acct_error(self):
            box.showerror("", "Account does not exist")

        def del_acct_success(self):
            box.showinfo("", "Account deleted")

        def change_pw_error(self):
            box.showerror("", "Invalid username and/or password")
        def change_pw_success(self):
            box.showinfo("", "Password changed")

        # usernameLabel = Label(self, text="Username:")
        # usernameLabel.grid(row=2, column=0, pady=5, padx=5)
        # usrTf = Entry(self)
        # usrTf.grid(row=2, column=1, columnspan=2, padx=5, sticky=E + W)
        #
        # passwordLabel = Label(self, text="Password:")
        # passwordLabel.grid(row=3, column=0, pady=5, padx=5)
        # pwTf = Entry(self, show="*")
        # pwTf.grid(row=3, column=1, columnspan=2, padx=5, sticky=E + W)

        del_acct_btn = Button(self, text="Delete Account", command=lambda: del_acct())
        del_acct_btn.grid(row=2, column=0)

        change_pw_btn = Button(self, text="Change Password", command=lambda: reset_pw())
        change_pw_btn.grid(row=3, column=0)

        view_info_btn = Button(self, text = "View User Info", command=lambda: view_user_info())
        view_info_btn.grid(row=4, column=0)

        view_sync_btn = Button(self, text = "View Sync Info", command=lambda: view_sync_info())
        view_sync_btn.grid(row=5, column=0)

        view_file_btn = Button(self, text = "View File Info", command=lambda: view_file_info())
        view_file_btn.grid(row=6, column=0)

    def centerWindow(self):
        w = 140
        h = 183

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
    root = Tk()
    root.option_add('*background', blue)
    root.option_add('*foreground', gray)
    root.option_add('*Button*background', 'white')
    root.option_add('*Entry*background', 'white')
    app = LoggedOut(root)
    root.mainloop()


if __name__ == '__main__':
    main()

