'''
Author: Miles Catlett
Date: 7/22/2022
File: create_db.py
I came up with this script to easily create the new database on the windows or ubuntu machines I have been using.
Unfortunately, I have to manually create a database when I use A2 Hosting.
'''
from dotenv import load_dotenv
import mysql.connector
import os
load_dotenv()

database = os.getenv("DB_DATABASE")
host = os.getenv("DB_HOSTNAME")
passwd = os.getenv("DB_PASSWORD")
user = os.getenv("DB_USERNAME")


def create_db():
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
    )
    my_cursor = mydb.cursor()
    my_cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in my_cursor]
    if database not in databases:
        my_cursor.execute("CREATE DATABASE " + database)
