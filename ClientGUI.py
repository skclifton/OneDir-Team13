import os
import tkFileDialog
import tkSimpleDialog
from ttk import Style
import tkMessageBox as box
import Client
import config
from Tkinter import *
from Tkinter import *

gray = "#363A37"
blue = "#639793"

darkGreen = "#4C9603"
lightGreen = "#C1FD86"

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

        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)
        self.rowconfigure(5, pad=3)

        onedirLabel = Label(self, text="OneDir Login", font='25')
        onedirLabel.grid(row=0, column=0, rowspan=2)

        usernameLabel = Label(self, text="Username:")
        usernameLabel.grid(row=2, column=0, pady=5, padx=5)

        usernameTF = Entry(self)
        usernameTF.grid(row=2, column=1, columnspan=2, padx=5, sticky=E + W)

        passwordLabel = Label(self, text="Password:")
        passwordLabel.grid(row=3, column=0, pady=5, padx=5)

        passwordTF = Entry(self, show="*")
        passwordTF.grid(row=3, column=1, columnspan=2, padx=5, sticky=E + W)

        createAcctBtn = Button(self, text="Create Account", command=lambda: createAcct(usernameTF.get(), passwordTF.get()))
        createAcctBtn.grid(row=4, column=1)

        loginBtn = Button(self, text="Login", command=lambda: login(usernameTF.get(), passwordTF.get()))
        loginBtn.grid(row=4, column=2)

        def createAcct(usr, pw):
            if not (usr == '' or pw == ''):
                cli = Client.Client()
                response = cli.create_account(usr, pw)
                if response == 'Account Exists':
                    createAcctError(self)
                else:
                    createAcctSuccess(self)
            else:
                error(self)

        def login(usr, pw):
            if not (usr == '' or pw == ''):
                cli = Client.Client()
                response = cli.login(usr, pw)
                if response is False:
                    loginError(self)
                else:
                    loggedin = Tk()
                    loggedin.option_add('*background', blue)
                    loggedin.option_add('*foreground', gray)
                    loggedin.option_add('*Button*background', 'white')
                    loggedin.option_add('*Entry*background', 'white')
                    app = LoggedIn(loggedin)
                    loggedin.mainloop()
                    # loggedout.destroy()

            else:
                error(self)

        # Dialogue box definitions
        def error(self):
            box.showerror("", "Enter a username and password")

        def createAcctError(self):
            box.showwarning("", "Account exists")

        def createAcctSuccess(self):
            box.showinfo("", "Account created")

        def loginError(self):
            box.showerror("", "Incorrect username or password")


    def centerWindow(self):
        w = 330 #317
        h = 150

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

class LoggedIn(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("")
        self.style = Style()
        Style().configure("TButton", padding=(0, 5, 0, 5))
        self.style.theme_use("default")
        self.centerWindow()
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(0, pad=5)

        self.rowconfigure(0, pad=20)
        self.rowconfigure(1, pad=5)
        self.rowconfigure(2, pad=5)
        self.rowconfigure(3, pad=5)
        self.rowconfigure(4, pad=5)
        self.rowconfigure(5, pad=5)


        onedirLabel = Label(self, text="OneDir", font='25')
        onedirLabel.grid(row=0, column=0)

        #6: change username\n7: change password
        self.pack(fill=BOTH, expand=1)

        # Change username
        changeUsrBtn = Button(self, text="Change username", command=self.changeUsr)
        changeUsrBtn.grid(row=1, column=0)

        # Change password
        changePwBtn = Button(self, text="Change password", command=self.changePw)
        changePwBtn.grid(row=2, column=0)

        # Create Backup
        backupBtn = Button(self, text="Create a Backup", command=self.backup)
        backupBtn.grid(row=3, column=0)

        # Restore Backup
        restorebBtn = Button(self, text="Restore from Backup", command=self.restore_from_backup)
        restorebBtn.grid(row=4, column=0)

        # Turn sync on and off
        self.sync = IntVar()
        syncCb = Checkbutton(self, text="Sync files", variable=self.sync, command=self.onSyncClick)
        syncCb.select()
        syncCb.grid(row=5, column=0)


    def onSyncClick(self):
        if self.sync.get() == 1:
            config.run = True
        else:
            config.run = False

    def changeUsr(self):
        new_usr = tkSimpleDialog.askstring(title="Change Username", prompt="New Username")
        if new_usr is not None:
            if new_usr is not "":
                cli = Client.Client()
                response = cli.change_username(config.username, config.password, new_usr)
                if response == 'success':
                    box.showinfo("", "Username changed")
            else:
                box.showinfo("", "You must enter a new username")

    def changePw(self):
        new_pw = tkSimpleDialog.askstring(title="Change Password", prompt="New Password", show="*")
        if new_pw is not None:
            if new_pw is not "":
                cli = Client.Client()
                response = cli.change_password(config.username, config.password, new_pw)
                if response == 'success':
                    box.showinfo("", "Password changed")
            else:
                box.showinfo("", "You must enter a new password")

    def backup(self):
        cli = Client.Client()
        response = cli.backup()
        if response == 'success':
            box.showinfo("",'Backup created successfully.')
        else:
            box.showinfo('','There was an error backing up your files.')

    def restore_from_backup(self):
        cli = Client.Client()
        response = cli.restore_backup()
        if response == 'success':
            box.showinfo('','Successfully restored from backup.')
        else:
            box.showinfo('',response)

    def centerWindow(self):
        w = 160#142
        h = 200

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
    if 'onedir' not in os.listdir(os.environ['HOME']):
        os.mkdir(os.environ['HOME'] + '/onedir')

    loggedout = Tk()
    loggedout.option_add('*background', blue)
    loggedout.option_add('*foreground', gray)
    loggedout.option_add('*Button*background', 'white')
    loggedout.option_add('*Entry*background', 'white')
    app = LoggedOut(loggedout)
    loggedout.mainloop()


if __name__ == '__main__':
    main()