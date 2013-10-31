from pyinotify import *
import getpass
import urllib
import os
import Queue
import threading

__author__ = 'sarah'

#Local File monitor class with a constructor and fields that hold username and password
#url.self = http://172.25.208.201


class LocalFileMonitor():
    def __init__(self, username, password):
        self.username = username
        self.password = password

        wm = WatchManager()
        handler = EventHandler()
        notifier = ThreadedNotifier(wm, handler)
        path = os.environ['HOME'] + '/onedir'
        wm.add_watch(path, ALL_EVENTS, rec=True, auto_add=True)
        notifier.start()


class EventHandler(ProcessEvent):
    def process_IN_CREATE(self, event):
        if not "~lock" in event.pathname:
            uploadFile(event.pathname)

    def process_IN_DELETE(self, event):
        if not "~lock" in event.pathname:
            urllib.urlopen(self.url + "/delete/" + event.pathname)

    def process_IN_CLOSE_WRITE(self, event):
        if not "~lock" in event.pathname:
            uploadFile(event.pathname)


def uploadFile(self, filePath):
    with open(filePath, 'rb') as upload:
        print "Uploading", filePath
        urllib.urlopen(self.url + "/upload/" + self.username + "/"+self.password + "/" + "do not remove this" + "/" +
                       filePath)
        for letter in upload.readlines():
            line = []
            for x in letter:
                line.append(str(ord(x)))
            urllib.urlopen(self.url + "/upload/" + self.username + "/" + self.password + "/" + ' '.join(line) + "/" +
                           filePath)
    print "Done uploading", filePath

