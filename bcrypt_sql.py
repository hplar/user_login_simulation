#!/usr/bin/env python

"""
Ralph 15-05-2016
Hashed salty passwords, stuffed in the database and retrieved to compare to user login input.
"""

import MySQLdb
import bcrypt
import textwrap
import base64
from time import sleep


class Users:
    def __init__(self, first_run=True):
        if first_run == True:
            print textwrap.dedent("""
            Welcome, choose an option.
            --------------------

            1. create user
            2. test user
            """)

        option = raw_input("Option: ")

        if option == "1":
            username, password = self.user_input()
            db, db_table, cursor = self.database_connect()
            self.create_user(db, db_table, cursor, username, password)
        elif option == "2":
            username, password = self.user_input()
            db, db_table, cursor = self.database_connect()
            self.test_user(db, db_table, cursor, username, password)
        else:
            print "\ntry again."
            sleep(1)
            Users(first_run=False)

    @staticmethod
    def user_input():
        username = str(raw_input("User: "))
        password = str(raw_input("Pass: "))
        return username, password

    @staticmethod
    def database_connect():
        db_user = base64.b64decode('aXRzbm90YW51c2Vy')
        db_password = base64.b64decode('aXRzbm90YXBhc3N3b3Jk')
        db_database = 'user_info'
        db_table = 'creds'
        db = MySQLdb.connect('localhost', db_user, db_password, db_database)
        cursor = db.cursor()
        return db, db_table, cursor

    @staticmethod
    def create_user(db, db_table, cursor, username, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        try:
            cursor.execute(
                "INSERT INTO creds (username, password, salt) VALUES (%s, %s, %s)", (username, hashed_password, salt))
            db.commit()
            print "\nInsert query applied successfully!"
            Users(1)
        except db.Error as error:
            print "\nFailed, reason below.\n %s" % error
            exit()
        db.close()

    @staticmethod
    def test_user(db, db_table, cursor, username, password):
        try:
            cursor.execute("SELECT password, salt FROM %s WHERE username = \"%s\"" % (db_table, username))
            retrieved_hashed_password, retrieved_salt = cursor.fetchone()
        except db.Error as error:
            print "Failed, reason below.\n\n %s" % error
            exit()
        db.close()
        if retrieved_hashed_password == bcrypt.hashpw(password, retrieved_salt):
            print "match"
        else:
            print "no match"
            exit()


if __name__ == "__main__":
    Users()
