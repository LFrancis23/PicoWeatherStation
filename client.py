#!/usr/bin/python3
import socket

HOST = "192.168.0.237"
PORT = 42069

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(b"Requesting Data")
    data = s.recv(1024)

print(f"Received {data!r}")
