__author__ = 'student'
import sqlite3
import getpass
import urllib
import csv, codecs, cStringIO
con = sqlite3.connect(":memory:")
c = con.cursor()
c.execute("create table accounts (usr, password)")

def add_account(self):
    is_running = True
    print "Enter blank line when prompted for username to exit."
    usr = raw_input("Enter new username: ")
    if usr == "":
        is_running = False
    while is_running is True:
        command = "select * from accounts where usr = '%s'" %usr
        c.execute(command)
        value = c.fetchone()
        while value != None:
            print "The specified email address already exists in the database."
            usr = raw_input("Enter email address: ")
            command = "select * from accounts where usr = '%s'" %usr
            c.execute(command)
            value = c.fetchone()
        pwd = getpass.getpass("Enter password: ")
        confirm_pwd = getpass.getpass("Confirm password: ")
        while pwd != confirm_pwd:
            print "Passwords do not match."
            pwd = getpass.getpass("Enter password: ")
            confirm_pwd = getpass.getpass("Confirm password: ")
        c.execute("insert into accounts values (?, ?)", (usr, pwd))
        print "Enter blank line when prompted for username to exit."
        usr = raw_input("Enter email address: ")
        if usr == "":
            is_running = False

def change_pwd(self):
    is_running = True
    print "Enter blank line when prompted for username to exit."
    usr = raw_input("Enter email address: ")
    if usr == "":
        is_running = False
    while is_running is True:
        command = "select * from accounts where usr = '%s'" %usr
        c.execute(command)
        value = c.fetchone()
        while value is None:
            print "The specified email does not exist in the database."
            usr = raw_input("Enter email address: ")
            command = "select * from accounts where usr = '%s'" %usr
            c.execute(command)
            value = c.fetchone()
        new_pwd = getpass.getpass("Enter new password:")
        confirm_pwd = getpass.getpass("Confirm new password:")
        while new_pwd != confirm_pwd:
            print "The entered passwords do not match."
            new_pwd = getpass.getpass("Enter new password:")
            confirm_pwd = getpass.getpass("Confirm new password:")
        command = "update accounts set password = '%s' where usr = '%s'" %(new_pwd, usr)
        c.execute(command)
        print "Enter blank line when prompted for username to exit."
        usr = raw_input("Enter email address: ")
        if usr == "":
            is_running = False

while True:
    print "Press 1 to add account."
    print "Press 2 to change password in account."
    print "Press any other button to exit."
    if raw_input() is not '1' or raw_input() is not '2':
        break
    if raw_input() == '1':
        add_account()
    if raw_input() == '2':
        change_pwd()



