from ttk import Style

__author__ = 'sarah'

from Tkinter import *

gray = "#626864"
blue = "#639793"

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background=gray)
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

        onedirLabel = Label(self, text="OneDir Login", background=gray, font='25', fg="white")
        onedirLabel.grid(row=0, column=0, rowspan=2)

        usernameLabel = Label(self, text="Username:", background=gray, fg="white")
        usernameLabel.grid(row=2, column=0, pady=5, padx=5)

        usernameTF = Entry(self)
        usernameTF.grid(row=2, column=1, columnspan=2, padx=5, sticky=E+W)

        passwordLabel = Label(self, text="Password:", background=gray, fg="white")
        passwordLabel.grid(row=3, column=0, pady=5, padx=5)

        passwordTF = Entry(self, show="*")
        passwordTF.grid(row=3, column=1, columnspan=2, padx=5, sticky=E+W)

        createAcctBtn = Button(self, text="Create Account", background=blue, fg="white")
        createAcctBtn.grid(row=4, column=1)

        loginBtn = Button(self, text="Login", background=blue, fg="white")
        loginBtn.grid(row=4, column=2)

        forgotPwBtn = Button(self, text="Reset Password", background=blue, fg="white")
        forgotPwBtn.grid(row=4, column=0)

        # abtn = Button(self, text="Activate")
        # abtn.grid(row=1, column=3)
        #
        # cbtn = Button(self, text="Close")
        # cbtn.grid(row=2, column=3, pady=4)
        #
        # hbtn = Button(self, text="Help")
        # hbtn.grid(row=5, column=0, padx=5)
        #
        # obtn = Button(self, text="OK")
        # obtn.grid(row=5, column=3)



        # frame = Frame(self, relief=RAISED, borderwidth=1)
        # frame.pack(fill=BOTH, expand=1)
        #
        # self.pack(fill=BOTH, expand=1)
        #
        # loginButton = Button(self, text="Login")
        # loginButton.pack(side=RIGHT, padx=2.5, pady=5)
        #
        # createAccountButton = Button(self, text='Create Account')
        # createAccountButton.pack(side=RIGHT, padx=2.5, pady=5)
        #
        # exitButton = Button(self, text="Exit", command=self.quit)
        # exitButton.pack(side=RIGHT, padx=2.5, pady=5)



    def centerWindow(self):
        w = 317
        h = 125

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

def main():
    root = Tk()
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()