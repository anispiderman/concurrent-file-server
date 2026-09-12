"""Minimal echo server used to introduce the socket lifecycle."""
import socket

HOST, PORT = "127.0.0.1", 65432
with socket.create_server((HOST, PORT)) as listener:
    connection, _ = listener.accept()
    with connection:
        while data := connection.recv(1024):
            connection.sendall(data)
