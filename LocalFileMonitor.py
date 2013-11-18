from pyinotify import *
import urllib
import Client
import thread
import config

class LocalFileMonitor():
    def __init__(self):

        wm = WatchManager()
        handler = EventHandler()
        self.notifier = ThreadedNotifier(wm, handler)
        directory = os.environ['HOME'] + '/onedir'
        wm.add_watch(directory, ALL_EVENTS, rec=True, auto_add=True)
        #notifier.start()
        thread.start_new_thread(self.notifier.loop, ())

class EventHandler(ProcessEvent):

    #def process_IN_CREATE(self, event):
    #    if not "~lock" in event.pathname:
    #       self.uploadFile(event.pathname)

    def process_IN_DELETE(self, event):
        if not "~lock" in event.pathname:
            urllib.urlopen(config.url + "/delete/" + config.username + '/' + config.password + '/' + event.pathname)

    def process_IN_MOVED_FROM(self, event):
        urllib.urlopen(config.url + '/delete/' + config.username + '/' + config.password + event.pathname)

    def process_IN_MOVED_TO(self, event):
        #urllib.urlopen(url + '/upload/' + username + '/' + password + event.pathname)
        if not '~lock' in event.pathname:
            Client.uploadFile(event.pathname)



    #def process_IN_ATTRIB(self, event):
    #    if not "~lock" in event.pathname:

    def process_IN_CLOSE_WRITE(self, event):
        if not "~lock" in event.pathname:
            Client.uploadFile(event.pathname)
