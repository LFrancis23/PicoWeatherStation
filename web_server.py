#Name: Landyn Francis
#File: web_server.py
#Purpose: Read sensors using I2C, and setup socket for incoming connections, send data to any incoming connections
import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
import bme280
from veml7700 import *

#WiFi Connection details intentionally removed
ssid = 0 
password = 0
#Initialize I2C object for each sensor
i2c = machine.I2C(0, scl=machine.Pin(9), sda = machine.Pin(8), freq = 10000)
i2c2 = machine.I2C(0, scl=machine.Pin(9), sda = machine.Pin(8), freq = 10000)
#Scan for i2c devices
devices = i2c.scan()

#Print each disocvered device
if devices:
    for d in devices:
        print(hex(d))
    
#Initialize the sensors
bme = bme280.BME280(i2c=i2c, address=0x77)
veml7700 = veml7700_init(i2c2)

#Serve data to a connection
def serve(connection):
    pico_led.off()
    while True:
        #Accept client connection
        client = connection.accept()[0]
        #Read request
        request = client.recv(1024)
        request = str(request)
        #Print request
        print(request)
        #Read VEML7700
        lux = veml7700_read(veml7700,i2c2)
        #Read BME280
        temp = bme.values[0]
        pressure = bme.values[1]
        humid = bme.values[2]
        
        #Send data in byte form
        client.send(f'{lux},{temp},{pressure},{humid}')
        #Close connection
        client.close()

def open_socket(ip):
    #Setup socket address
    address = (ip,42069)
    #Create socket
    connection = socket.socket()
    #Bind socket to address
    connection.bind(address)
    #Listen for incoming connections
    connection.listen(1)
    #Print connection details
    print(connection)
    return connection

def connect():
    #Connect to WLAN network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid,password)
    #Try connection every second (**Currently no timeout**)
    while wlan.isconnected() == False:
        print("waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    #Print IP address
    print(f'Connected on {ip}')
    return ip
    
try:
    #Get IP address by connecting to WLAN network
    ip = connect()
    #Get socket, await connections
    connection = open_socket(ip)
    #Serve data to a connectec client
    serve(connection)
    
except KeyboardInterrupt:
    machine.reset()