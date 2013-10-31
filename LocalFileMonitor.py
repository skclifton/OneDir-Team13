from pyinotify import *
import getpass
import urllib
import Queue
import thread
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
        directory = '/home/' + getpass.getuser() + '/onedir'
        wm.add_watch(directory, ALL_EVENTS, rec=True, auto_add=True)
        #notifier.start()
        thread.start_new_thread(notifier.loop, ())


class EventHandler(ProcessEvent):
    def process_IN_CREATE(self, event):
        if not "~lock" in event.pathname:
            uploadFile(event.pathname)

    def process_IN_DELETE(self, event):
        if not "~lock" in event.pathname:
            urllib.urlopen(self.url + "/delete/" + event.pathname)

    def process_IN_ATTRIB(self, event):
        if not "~lock" in event.pathname:
            print "changing metadata for", event.pathname

    def process_IN_CLOSE_WRITE(self, event):
        if not "~lock" in event.pathname:
            uploadFile(event.pathname)


def uploadFile(self, filePath):
    with open(filePath, 'rb') as upload:
        print "Uploading", filePath
        urllib.urlopen(self.url+"/upload/"+self.username+"/"+self.password+"/"+filePath+"/"+"do not remove this")
        for letter in upload.readlines():
            line = []
            for x in letter:
                line.append(str(ord(x)))
            urllib.urlopen(self.url+"/upload/"+self.username+"/"+self.password+"/"+filePath+"/"+' '.join(line))
    print "Done uploading", filePath