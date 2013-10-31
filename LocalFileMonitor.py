from pyinotify import *
import getpass
import urllib
import Queue
import threading

__author__ = 'sarah'

url = 'http://172.25.208.149:5000'
username = ''
password = ''

class LocalFileMonitor():
    def __init__(self, un, pw):
        username = un
        password = pw


class EventHandler(ProcessEvent):
    def process_IN_CREATE(self, event):
        if not "~lock" in event.pathname:
            uploadFile(event.pathname)

    def process_IN_DELETE(self, event):
        if not "~lock" in event.pathname:
            deleteFile(event.pathname)

    def process_IN_ATTRIB(self, event):
        if not "~lock" in event.pathname:
            print "changing metadata for", event.pathname

    def process_IN_CLOSE_WRITE(self, event):
        if not "~lock" in event.pathname:
            uploadFile(event.pathname)


def uploadFile(filePath):
    with open(filePath, 'rb') as upload:
        print "Uploading", filePath
        urllib.urlopen(url+"/upload/"+username+"/"+password+"/"+filePath+"/"+"do not remove this")
        for letter in upload.readlines():
            line = []
            for x in letter:
                line.append(str(ord(x)))
            urllib.urlopen(url+"/upload/"+username+"/"+password+"/"+filePath+"/"+' '.join(line))
    print "Done uploading", filePath


def deleteFile(filePath):
    urllib.urlopen(url + "/delete/" + filePath)


wm = WatchManager()
handler = EventHandler()
notifier = ThreadedNotifier(wm, handler)
directory = '/home/' + getpass.getuser() + '/onedir'
wm.add_watch(directory, ALL_EVENTS, rec=True, auto_add=True)
notifier.start()