from flask import Flask
import sqlite3
import os
import time

app = Flask(__name__)
path = os.environ['HOME'] + "/onedir"

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

from signal import SIG_DFL, SIGPIPE, signal
signal(SIGPIPE,SIG_DFL)

con = sqlite3.connect("accounts.db", check_same_thread=False)
con.isolation_level = None
c = con.cursor()
#h = open('history.txt', 'r+')

if not 'history.txt' in os.listdir(path):
    with open(path + '/history.txt', 'w+'):
        pass

h = open(path + '/history.txt', 'r+')

c.execute("create table if not exists accounts (usr, password)")

@app.route('/account/<username>/<password>')
def create_account(username, password):
    command = "select * from accounts where usr = '%s'" % username
    c.execute(command)
    value = c.fetchone()

    if not value is None:
        return 'exists' #"The specified email address already exists in the database."

    #pw = getpass.getpass("New Password: ")
    #confirm_pw = getpass.getpass("Confirm Password: ")
    c.execute("insert into accounts values (?, ?)", (username, password))
    return 'created'


@app.route("/delete/<username>/<password>/<path:file>")
def delete(username, password, file):
    if login(username, password) != "success":
        return 'failure'
    else:
        file = file.split('/')
        file.pop(0)
        file.pop(0)
        file.pop(0)
        filename = file.pop()
        filepath = '/'.join(file)
        filepath = path + '/' + username + '/' + filepath

        os.chdir(filepath)
        if file in os.listdir(os.getcwd()):
            print 'file removed: ' + filename
            os.remove(file)
            return 'success'
        return 'failure'

@app.route("/upload/<username>/<password>/<data>/<path:file>")
def upload(username, password, data, file):
    #print "Upload called on server"
    c = con.cursor()
    if login(username, password) != "success":
        return 'failure'
    else:
        #print 'Initial filepath: ' + file

        file = file.split('/')
        file.pop(0) # remove home
        file.pop(0) # remove user profile (usually student)
        file.pop(0) # remove onedir (it's already in path)
        #print file
        filename = file.pop()
        #print 'Changed to: ' + str(file)
        filepath = '/'.join(file)
        filepath = path + '/' + username + '/' + filepath
        h.write("Upload | User: " + username + " Filepath: " + filepath + "\n")

        #print 'Attempting to upload ' + filename + ' at ' + filepath
        #print 'Path exists? ' + str(os.path.exists(filepath))
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        #print 'Path made? ' + str(os.path.exists(filepath))

        os.chdir(filepath) #change the current directory to where we're uploading
        #print 'File in filepath? ' + str(filename in os.listdir(os.getcwd()))
        #if filename not in os.listdir(os.getcwd()): #if filename not in the filepath
        #    #print 'opening file' + filename

        if data == '\0':
            with open(filename, 'w') as fix:
                pass

            return 'success'

        upload = open(filename, 'ab')
        #print "Writing line: " + data
        data = data.split()
        for data in data:
            upload.write(chr(int(data)))
        upload.close()

        return 'success'


@app.route('/changepw/<username>/<password>/<new_password>')
def change_password(username, password, new_password):
    if not login(username, password):
        return 'failure'

    command = "UPDATE accounts SET password = '%s' WHERE usr = '%s'" %(new_password, username)
    c.execute(command)
    return 'success'

@app.route('/changeusr/<username>/<password>/<new_usr>')
def change_username(username, password, new_usr):
    if not login(username, password):
        return 'failure'

    command = "UPDATE accounts SET usr = '%s' WHERE usr = '%s'" %(new_usr, username)
    c.execute(command)

    if os.path.exists(path + '/' + username):
        os.rename(path + '/' + username, path + '/' + new_usr)

    return 'success'

@app.route('/login/<username>/<password>')
def login(username, password):
    command = "select * from accounts where usr = '%s' AND password = '%s'" %(username, password)
    c.execute(command)
    #c.execute("select * from accounts where usr = ? AND password = ?" (username, password))
    value = c.fetchone()
    #print value
    if value is None:
        return "failure"
    else:
        return "success"

@app.route('/list/<username>/<password>')
def list(username, password):
    #(dirpath, dirnames, filenames) for each file and directory
    list_of_directories = os.walk(path + '/' + username) # walk through the user's files
    output = ''
    for files_and_directories in list_of_directories:
        directory = files_and_directories[0]
        for file in files_and_directories[2]:
            # add the full filepath for each file on the server in the user's folder
            output += directory + '/' + file + '\0'#'<br />'
    return output

@app.route('/lastmodified/<path:file2>')
def last_modified(file2):
    #print 'routed to lastmodified'
    if os.path.exists(file2):
        return str(os.path.getmtime(file2))
    else:
        return str(time.time())

@app.route('/download/<username>/<password>/<path:file>')
def download(username, password, file):
    server_path = file.split('/')
    server_path.pop(0) # home
    server_path.pop(0) # user
    server_path.pop(0) # onedir
    server_path = '/'.join(server_path)
    with open(path + '/' + username + '/' + server_path) as server_file:
        return server_file.read()

@app.route('/userinfo')
def userinfo():
    retStr = 'Username\t\tPassword\n'
    command = "SELECT usr from accounts"
    c.execute(command)
    i = 0
    user = c.fetchone()
    while user is not None:
        retStr += user[0] + '\t\t' + user[1]
    return retStr

@app.route('/fileinfo')
def fileinfo():
    retStr = 'User: \nUser\t\tFile Size\t\tFile Count\n'
    totalsize = 0
    totalcount = 0
    command = "SELECT usr from accounts"
    c.execute(command)
    i = 0
    user = c.fetchone()
    while user is not None:
        usersize = 0
        usercount = 0
        for root, dirs, files in os.walk(path + '/' + user[0]):
            for name in files:
                totalsize += os.path.getsize(name)
                totalcount += 1
                usersize += os.path.getsize(name)
                usercount += 1
        retStr += user[0] + "\t\t" + str(usersize) + "\t\t" + str(usercount) + "\n"
        user = c.fetchone()
        i += 1

    retStr += 'Total: \n' + 'File Size: ' + str(totalsize) + '\tFile Count: ' + str(totalcount)
    return retStr

@app.route('/synchistory')
def synchistory():
    historyStr = ''
    for line in h:
        historyStr += line
    return historyStr

if __name__ == '__main__':
    if 'onedir' not in os.listdir(os.environ['HOME']):
        os.mkdir(path)
    #app.run()
    app.run(host = '0.0.0.0', debug = False)
