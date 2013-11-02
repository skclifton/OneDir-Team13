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
        self.notifier.stop()

    def start_sync(self):
        thread.start_new_thread(self.notifier.loop, ())


class EventHandler(ProcessEvent):

    def process_IN_CREATE(self, event):
        if not "~lock" in event.pathname:
            self.uploadFile(event.pathname)

    def process_IN_DELETE(self, event):
        if not "~lock" in event.pathname:
            urllib.urlopen(self.url + "/delete/" + event.pathname)

    def process_IN_ATTRIB(self, event):
        if not "~lock" in event.pathname:
            print "changing metadata for", event.pathname

    def process_IN_CLOSE_WRITE(self, event):
        if not "~lock" in event.pathname:
            self.uploadFile(event.pathname)


    def uploadFile(self, filePath):
        with open(filePath, 'rb') as upload:
            print "Uploading", filePath
            urllib.urlopen(url+"/upload/"+username+"/"+password+'/'+"do not remove this" + filePath)
            for letter in upload.readlines():
                line = []
                for x in letter:
                    line.append(str(ord(x)))
                urllib.urlopen(url+"/upload/"+username+"/"+password+"/" + ' '.join(line) + filePath)
        print "Done uploading", filePath
