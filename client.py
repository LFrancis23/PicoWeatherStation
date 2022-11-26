#!/usr/bin/python3
import socket
import sqlite3
from datetime import datetime
import time
import re

HOST = "192.168.0.237"
PORT = 42069


def getDateTime():
	now = datetime.now()#Get current datetime
	now = now.isoformat() #Convert datetime to iso format
	return now

def read_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        s.sendall(b"Requesting Data")
        data = s.recv(1024)
        data = data.decode("utf-8").split(',')
    return data



data = read_data()

lux = data[0]
temp = data[1]
temp = temp[:-1]
pressure = data[2]
pressure = pressure[:-3]
humidity = data[3]
humidity = humidity[:-1]
now = getDateTime()
print(lux,temp,pressure,humidity)
try:
    sqliteConnection = sqlite3.connect('/var/www/datalogger/weatherstation.db')
    cursor = sqliteConnection.cursor()
    print ("Successfully connected to SQLITE")
    cursor.execute("CREATE TABLE IF NOT EXISTS weather (lux REAL,temperature REAL,pressure REAL,humid REAL,datetime TEXT);")
    sqliteConnection.commit()
    print ("Successfully created table")
    #Insert into table
    count = cursor.execute("""INSERT INTO weather 
                        (lux, temperature, pressure, humid, datetime) 
                        VALUES (?,?,?,?,?)""",
                        (lux,temp,pressure,humidity,now))
    sqliteConnection.commit()
    print("Record inserted successfully into weather table", cursor.rowcount)
    cursor.close()
except sqlite3.Error as error:
    print("Error while creating sqlite table",error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite Connection is closed")