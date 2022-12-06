#!/usr/bin/python3
#Name: Landyn Francis
#File: client.py
#Purpose: Connect to Pico W using a TCP socket, store data in SQLite3 database.
import socket
import sqlite3
from datetime import datetime
import time
import re

# Address of Pico W
HOST = "192.168.0.237"
PORT = 42069

#Get current datetime
def getDateTime():
    now = datetime.now()  # Get current datetime
    now = now.isoformat()  # Convert datetime to iso format
    return now

#Make socket connection to Pico W and read data
def read_data():
    #Create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #Connect to Pico W
        s.connect((HOST, PORT))
        #Send data
        s.sendall(b"Requesting Data")
        #Receive sensor data
        data = s.recv(1024)
        #Decode data to utf-8, and split on commas
        data = data.decode("utf-8").split(",")
        #Return data as list
    return data

#Read data
data = read_data()

#Lux is first value
lux = data[0]
#Temp is second value (trim units)
temp = data[1]
temp = temp[:-1]
#Pressure is third value (trim units)
pressure = data[2]
pressure = pressure[:-3]
#Humiditiy is fourth value (trim units)
humidity = data[3]
humidity = humidity[:-1]
#Get current date and time
now = getDateTime()
#Print sensor data
print(lux, temp, pressure, humidity)
try:
    #Connect to a SQLite database
    sqliteConnection = sqlite3.connect("/var/www/datalogger/weatherstation.db")
    #Create a cursor
    cursor = sqliteConnection.cursor()
    print("Successfully connected to SQLITE")
    #Create a table if it does not already exist
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS weather (lux REAL,temperature REAL,pressure REAL,humid REAL,datetime TEXT);"
    )
    sqliteConnection.commit()
    print("Successfully created table")
    # Insert into table
    count = cursor.execute(
        """INSERT INTO weather 
                        (lux, temperature, pressure, humid, datetime) 
                        VALUES (?,?,?,?,?)""",
        (lux, temp, pressure, humidity, now),
    )
    sqliteConnection.commit()
    print("Record inserted successfully into weather table", cursor.rowcount)
    #Close cursor
    cursor.close()
except sqlite3.Error as error:
    print("Error while creating sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite Connection is closed")
