import time
import machine
import socket
import network
import rp2

rp2.country('US')
ssid = "Telephone Line"
password = "ElectricLightsOrchestra"
led = machine.Pin("LED",machine.Pin.OUT)
HOST = "127.0.0.1"
PORT = 69420

html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title></head>
    <body> <h1> Pico W</h1>
        <p>Hello World data = %d</p>
    </body>
</html>
"""

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid,password)

max_wait = 60
while max_wait > 0:
    if wlan.status() > 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)
    
while True:
    try:
        cl, addr = s.accept()
        print('client connected from',addr)
        cl_file = cl.makefile('rwb',0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        data = 5
        response = html % data
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
    except OSerror as e:
        cl.close()
        print('connection closed')
    


