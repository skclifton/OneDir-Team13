__author__ = 'piammoradi'
import sqlite3
import getpass
import urllib
import csv, codecs, cStringIO
con = sqlite3.connect("example2.db")
c = con.cursor()
c.execute("create table if not exists accounts (email, password)")
while True:
    print "Enter 1 to add account."
    print "Enter 2 to change password."
    print "Enter 3 to delete account."
    print "Press anything else to exit."
    option = raw_input()
    if option is not '1' and option is not '2' and option is not '3':
        break
    else:
        while option == '1':
            print "Enter blank line to exit."
            email = raw_input("Enter email address: ")
            if email == "":
                break
            command = "select * from accounts where email = '%s'" %email
            c.execute(command)
            value = c.fetchone()
            while value != None:
                 print "The specified email address already exists in the database."
                 print "Enter blank line to exit."
                 email = raw_input("Enter email address: ")
                 if email == '':
                     option = ''
                     break
                 command = "select * from accounts where email = '%s'" %email
                 c.execute(command)
                 value = c.fetchone()
                #break
            if option != '1':
                break
            password = getpass.getpass("Enter password: ")
            confirm = getpass.getpass("Confirm password: ")
            while password != confirm:
                print "Passwords do not match."
                password = getpass.getpass("Enter password: ")
                confirm = getpass.getpass("Confirm password: ")
            c.execute("insert into accounts values (?, ?)", (email, password))
            con.commit()
        while option == '2':
            print ("Enter blank line to exit.")
            email = raw_input("Enter username: ")
            if email == "":
                break
            pwd = getpass.getpass("Enter password: ")
            command = "select * from accounts where email = '%s'" %(email)
            c.execute(command)
            value = c.fetchone()
            while value is None:
                print "The specified username does not exist."
                print "Enter blank line to eixt."
                email = raw_input("Enter username: ")
                if email == "":
                    option == ''
                    break
                pwd = getpass.getpass("Enter password: ")
                command = "select * from accounts where email = '%s'" %(email)
                c.execute(command)
                value = c.fetchone()
            if option != '2':
                break
            command = "select * from accounts where email = '%s' and password = '%s'" %(email, pwd)
            c.execute(command)
            value = c.fetchone()
            while value is None:
                print "Incorrect password."
                email = raw_input("Enter username: ")
                pwd = getpass.getpass("Enter password: ")
                command = "select * from accounts where email = '%s'" %(email)
                c.execute(command)
                value = c.fetchone()
            new_pwd = getpass.getpass("Enter new password: ")
            confirm_pwd = getpass.getpass("Confirm new password: ")
            while new_pwd != confirm_pwd:
                print "The given passwords do not match."
                new_pwd = getpass.getpass("Enter new password: ")
                confirm_pwd = getpass.getpass("Confirm new password: ")
            command = "update accounts set password = '%s' where email = '%s'" %(new_pwd, email)
            c.execute(command)
            con.commit()
        while option == '3':
            print ("Enter blank line to exit.")
            email = raw_input("Enter username of account you would like to delete: ")
            if email == "":
                break
            command = "select * from accounts where email = '%s'" %(email)
            c.execute(command)
            value = c.fetchone()
            while value is None:
                print "The specified username does not exist."
                print "Enter blank line to exit."
                email = raw_input("Enter username of account you would like to delete: ")
                if email == "":
                    option = ''
                    break
                command = "select * from accounts where email = '%s'" %(email)
                c.execute(command)
                value = c.fetchone()
            if option != '3':
                break
            command = "delete from accounts where email = '%s'" %(email)
            c.execute(command)
            con.commit()
con.close()
