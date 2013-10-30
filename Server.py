from flask import Flask
import sqlite3
import os
#commen
app = Flask(__name__)

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

con = sqlite3.connect(":memory:")
c = con.cursor()
c.execute("create table accounts (usr, password)")

@app.route('/')
def hello():
    return "hello world"

@app.route('/test/<arg>')
def test(arg):
    return arg

@app.route('/account/<username>/<password>')
def create_account(username, password):
    command = "select * from accounts where usr = '%s'" % username
    c.execute(command)
    value = c.fetchone()

    if value != None:
        return 'exists' #"The specified email address already exists in the database."

    #pw = getpass.getpass("New Password: ")
    #confirm_pw = getpass.getpass("Confirm Password: ")
    c.execute("insert into accounts values (?, ?)", (username, password))
    #with open('accounts.txt', 'a+b') as accounts:
    #    accounts.write(username + ' ' + password + "\n")
    #users[username] = password #temporary until the server is restarted and user info is reloaded
    return 'created'


@app.route("/upload/<username>/<password>/<file>/<data>")
def upload(username, password, file, data):
    if login(username, password) is False:
        return 'failure'
    else:
        if file not in os.listdir("onedir"):
            with open("onedir/"+file, 'w') as file:
                pass
        upload = open("onedir/"+file, 'ab')
        #print "Writing line: " + data
        data = data.split()
        for data in data:
            upload.write(chr(int(data)))
        upload.close()
        return 'success'


@app.route('/login/<username>/<password>')
def login(username, password):
    command = "select * from accounts where usr = '%s' and pw = '%s'" % username, password
    c.execute(command)
    value = c.fetchone()
    if value is None:
        return "failure"
    else:
        return "success"

if __name__ == '__main__':
    if 'onedir' not in os.listdir(os.getcwd()):
        os.mkdir("onedir")
    #app.run()
    app.run(host = '0.0.0.0', debug = False)
