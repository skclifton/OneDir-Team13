from pyinotify import *
import getpass
import urllib
import os
import Queue
import threading

__author__ = 'sarah'

#Local File monitor class with a constructor and fields that hold username and password
#url.self = http://172.25.208.201

path = os.environ['HOME'] + '/onedir'

class LocalFileMonitor():
    def __init__(self, username, password):
        self.username = username
        self.password = password

        thread_list = []
        wm = WatchManager()
        self.handler = EventHandler()
        self.notifier = Notifier(wm, self.handler)
        wm.add_watch(path, ALL_EVENTS, rec=True, auto_add=True)

    '''
    def update(self):
        print "Updating LFM"
        self.notifier.process_events()
        if self.notifier.check_events():
            self.notifier.read_events()

        print self.handler.files + " test"
        while self.handler.files:
            uploadFile(self.handler.files.pop())
    '''

class EventHandler(ProcessEvent):
    files = set()
    def process_IN_CREATE(self, event):
        self.files.add(event.pathname)
        if not "~lock" in event.pathname:
            print "creating", event.pathname
        # if directory

    def process_IN_DELETE(self, event):
        # if not "~lock" in event.pathname:
            print "deleting", event.pathname

    def process_IN_ACCESS(self, event):
        # if not "~lock" in event.pathname:
            print "accessing", event.pathname

    def process_IN_ATTRIB(self, event):
        # if not "~lock" in event.pathname:
            print "changing metadata for", event.pathname

    def process_IN_OPEN(self, event):
        # if not "~lock" in event.pathname:
            print "opening", event.pathname

    def process_IN_CLOSE_WRITE(self, event):
        self.files.add(event.pathname)
        if not "~lock" in event.pathname:
            print "closing", event.pathname
            # filePath = event.pathname
            # thread = threading.Thread(target=uploadFile, args=(filePath,))
            # thread_list.append(thread)
            # for thread in thread_list:
            #     thread.start()

    def process_IN_MODIFY(self, event):
        self.files.add(event.pathname)
        if not "~lock" in event.pathname:
            print "modified", event.pathname
        #add pathname to end of list if not already in list


def uploadFile(self, filePath):
    with open(filePath, 'rb') as upload:
        print "Uploading", filePath
        urllib.urlopen(self.url+"/upload/"+self.username+"/"+self.password+"/" + "do not remove this" + "/" + filePath)
        for letter in upload.readlines():
            line = []
            for x in letter:
                line.append(str(ord(x)))
            urllib.urlopen(self.url+"/upload/"+self.username+"/"+self.password+"/" + ' '.join(line) + "/" + filePath)
    print "Done uploading", filePath


