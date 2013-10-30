from flask import Flask
import sqlite3
import os

app = Flask(__name__)
path = os.environ['HOME']
print path

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

con = sqlite3.connect(":memory:", check_same_thread=False)
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
    return 'created'


@app.route("/upload/<username>/<password>/<data>/<path:file>")
def upload(username, password, data, file):
    if login(username, password) != "success":
        return 'failure'
    else:
        if file not in os.listdir(path + "onedir"):
            with open(path + "onedir/"+file, 'w') as file:
                pass
        upload = open(path + "onedir/"+file, 'ab')
        #print "Writing line: " + data
        data = data.split()
        for data in data:
            upload.write(chr(int(data)))
        upload.close()
        return 'success'


@app.route('/login/<username>/<password>')
def login(username, password):
    command = "select * from accounts where usr = '%s' AND password = '%s'" %(username, password)
    c.execute(command)
    #c.execute("select * from accounts where usr = ? AND password = ?" (username, password))
    value = c.fetchone()
    print value
    if value is None:
        return "failure"
    else:
        return "success"

if __name__ == '__main__':
    if 'onedir' not in path:#os.listdir(os.getcwd()):
        os.mkdir(path + "/onedir")
    #app.run()
    app.run(host = '0.0.0.0', debug = True)
    app.path = path + "/onedir"
