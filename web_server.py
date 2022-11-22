import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
import bme280
from veml7700 import *

ssid = "Telephone Line"
password = "ElectricLightsOrchestra"
i2c = machine.I2C(0, scl=machine.Pin(9), sda = machine.Pin(8), freq = 10000)
i2c2 = machine.I2C(0, scl=machine.Pin(9), sda = machine.Pin(8), freq = 10000)

devices = i2c.scan()

if devices:
    for d in devices:
        print(hex(d))
            
bme = bme280.BME280(i2c=i2c, address=0x77)
veml7700 = veml7700_init(i2c2)


def serve(connection):
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)
        lux = veml7700_read(veml7700,i2c2)
        temp = bme.values[0]
        pressure = bme.values[1]
        humid = bme.values[2]
        
        client.send(f'{lux},{temp},{pressure},{humid}')
        client.close()

def open_socket(ip):
    address = (ip,42069)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid,password)
    while wlan.isconnected() == False:
        print("waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
    
except KeyboardInterrupt:
    machine.reset()