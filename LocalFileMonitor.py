from pyinotify import *
import getpass
import urllib
import Queue
import thread
import threading
import Client

__author__ = 'sarah'

#Local File monitor class with a constructor and fields that hold username and password
#url.self = http://172.25.208.201

global username
global password
global url
global run
run = True


class LocalFileMonitor():
    def __init__(self, un, pw, u):
        global username
        username = un

        global password
        password = pw

        global url
        url = u

        wm = WatchManager()
        handler = EventHandler()
        self.notifier = ThreadedNotifier(wm, handler)
        directory = os.environ['HOME'] + '/onedir'
        wm.add_watch(directory, ALL_EVENTS, rec=True, auto_add=True)
        #notifier.start()
        thread.start_new_thread(self.notifier.loop, ())

    def stop_sync(self):
        global run
        run = False

    def start_sync(self):
        #thread.start_new_thread(self.notifier.loop, ())
        global run
        run = True

    def set_username(self, new_username):
        global username
        username = new_username

    def set_password(self, new_password):
        global password
        password = new_password


class EventHandler(ProcessEvent):

    #def process_IN_CREATE(self, event):
    #    if not "~lock" in event.pathname:
    #       self.uploadFile(event.pathname)

    def process_IN_DELETE(self, event):
        if not "~lock" in event.pathname:
            urllib.urlopen(url + "/delete/" + username + '/' + password + '/' + event.pathname)

    def process_IN_MOVED_FROM(self, event):
        urllib.urlopen(url + '/delete/' + username + '/' + password + event.pathname)

    def process_IN_MOVED_TO(self, event):
        #urllib.urlopen(url + '/upload/' + username + '/' + password + event.pathname)
        if not '~lock' in event.pathname:
            self.uploadFile(event.pathname)


    #def process_IN_ATTRIB(self, event):
    #    if not "~lock" in event.pathname:

    def process_IN_CLOSE_WRITE(self, event):
        if not "~lock" in event.pathname:
            self.uploadFile(event.pathname)

    def uploadFile(self, filePath):
        if run:
            with open(filePath, 'rb') as upload:
                urllib.urlopen(url+"/upload/"+username+"/"+password+'/'+"\0" + filePath)
                for letter in upload.readlines():
                    line = []
                    for x in letter:
                        line.append(str(ord(x)))
                    urllib.urlopen(url+"/upload/"+username+"/"+password+"/" + ' '.join(line) + filePath)
