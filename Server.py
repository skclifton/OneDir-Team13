from flask import Flask
import os
#commen
app = Flask(__name__)

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

users = {}
with open('../OneDir2/accounts.txt') as accounts:
    for line in accounts:
        data = line.strip().split(' ')
        users[data[0]] = data[1]

@app.route('/')
def hello():
    return "hello world"

@app.route('/test/<arg>')
def test(arg):
    return arg

@app.route('/account/<username>/<password>')
def create_account(username, password):
    with open('../OneDir2/accounts.txt', 'a+b') as accounts:
        accounts.write(username + ' ' + password + "\n")
    users[username] = password #temporary until the server is restarted and user info is reloaded
    return 'Account Created.'




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
    if username not in users:
        return "failure"
    if users[username] == password:
        return "success"
    else:
        return "failure"

if __name__ == '__main__':
    if 'onedir' not in os.listdir(os.getcwd()):
        os.mkdir("onedir")
    #app.run()
    app.run(host = '0.0.0.0', debug = False)
