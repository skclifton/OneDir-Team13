__author__ = 'piammoradi'
import sqlite3
import getpass
import urllib
import csv, codecs, cStringIO
con = sqlite3.connect(":memory:")
c = con.cursor()
c.execute("create table accounts (email, password)")
while True:
    print "Enter blank line to exit."
    email = raw_input("Enter email address: ")
    if email == "":
        break
    command = "select * from accounts where email = '%s'" % email
    c.execute(command)
    value = c.fetchone()
    while value != None:
         print "The specified email address already exists in the database."
         email = raw_input("Enter email address: ")
         command = "select * from accounts where email = '%s'" % email
         c.execute(command)
         value = c.fetchone()
        #break
    if email == "":
        break
    password = getpass.getpass("Enter password: ")
    confirm = getpass.getpass("Confirm password: ")
    while password != confirm:
        print "Passwords do not match."
        password = getpass.getpass("Enter password: ")
        confirm = getpass.getpass("Confirm password: ")
    c.execute("insert into accounts values (?, ?)", (email, password))





