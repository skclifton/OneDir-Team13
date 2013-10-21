__author__ = 'sarah'

from pyinotify import *
import getpass

__author__ = 'sarah'

class EventHandler(ProcessEvent):
        def process_IN_CREATE(self, event):
            if not "~lock" in event.pathname:
                print "creating", event.pathname

        def process_IN_DELETE(self, event):
            if not "~lock" in event.pathname:
                print "deleting", event.pathname

        # def process_IN_ACCESS(self, event):
        #     if not "~lock" in event.pathname:
        #         print "accessing", event.pathname

        def process_IN_ATTRIB(self, event):
            if not "~lock" in event.pathname:
                print "changing metadata for", event.pathname

        def process_IN_OPEN(self, event):
            if not "~lock" in event.pathname:
                print "opening", event.pathname

        def process_IN_CLOSE_WRITE(self, event):
            if not "~lock" in event.pathname:
                print "closing", event.pathname

handler = EventHandler()
wm = WatchManager()
notifier = Notifier(wm, handler)
directory = '/home/' + getpass.getuser() + '/onedir'
wm.add_watch(directory, ALL_EVENTS)
notifier.loop()
