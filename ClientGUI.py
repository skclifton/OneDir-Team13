from ttk import Style
import tkMessageBox as box
import LocalFileMonitor
import Server
import Admin
import Client

__author__ = 'sarah'

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

        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)

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
                    loggedin.option_add('*background', gray)
                    loggedin.option_add('*foreground', 'white')
                    loggedin.option_add('*Button*background', blue)
                    loggedin.option_add('*Entry*background', 'white')
                    loggedin.option_add('*Entry*foreground', blue)
                    app = LoggedIn(loggedin)
                    loggedin.mainloop()
            else:
                error(self)

        def forgotPw(usr):
            print 'how do we want to handle this?'

        createAcctBtn = Button(self, text="Create Account", command=lambda: createAcct(usernameTF.get(), passwordTF.get()))
        createAcctBtn.grid(row=4, column=1)

        loginBtn = Button(self, text="Login", command=lambda: login(usernameTF.get(), passwordTF.get()))
        loginBtn.grid(row=4, column=2)

        forgotPwBtn = Button(self, text="Reset Password", command=forgotPw)
        forgotPwBtn.grid(row=4, column=0)

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
        w = 317
        h = 125

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
        self.parent.title("Under Construction")
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

        onedirLabel = Label(self, text="Under Construction", font='25')
        onedirLabel.grid(row=0, column=0, rowspan=2)

    def centerWindow(self):
        w = 317
        h = 125

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
    root = Tk()
    root.option_add('*background', gray)
    root.option_add('*foreground', 'white')
    root.option_add('*Button*background', blue)
    root.option_add('*Entry*background', 'white')
    root.option_add('*Entry*foreground', blue)
    app = LoggedOut(root)
    root.mainloop()


if __name__ == '__main__':
    main()