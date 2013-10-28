from pyinotify import *
import getpass
import urllib
import Queue
import threading

__author__ = 'sarah'

#Local File monitor class with a constructor and fields that hold username and password
#url.self = http://172.25.208.201


class LocalFileMonitor():
    def __init__(self, username, password):
        self.username = username
        self.password = password


class EventHandler(ProcessEvent):
    def process_IN_CREATE(self, event):
        # if not "~lock" in event.pathname:
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
        if not "~lock" in event.pathname:
            print "closing", event.pathname
            # filePath = event.pathname
            # thread = threading.Thread(target=uploadFile, args=(filePath,))
            # thread_list.append(thread)
            # for thread in thread_list:
            #     thread.start()

    def process_IN_MODIFY(self, event):
        if not "~lock" in event.pathname:
            print "modified", event.pathname
        #add pathname to end of list if not already in list


# def uploadFile(self, filePath):
#     with open(filePath, 'rb') as upload:
#         print "Uploading", filePath
#         urllib.urlopen(self.url+"/upload/"+self.username+"/"+self.password+"/"+filePath+"/"+"do not remove this")
#         for letter in upload.readlines():
#             line = []
#             for x in letter:
#                 line.append(str(ord(x)))
#             urllib.urlopen(self.url+"/upload/"+self.username+"/"+self.password+"/"+filePath+"/"+' '.join(line))
#     print "Done uploading", filePath

thread_list = []
wm = WatchManager()
handler = EventHandler()
notifier = Notifier(wm, handler)
directory = '/home/' + getpass.getuser() + '/onedir'
wm.add_watch(directory, ALL_EVENTS, rec=True, auto_add=True)

notifier.loop()
