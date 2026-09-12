"""Client for echo-server.py."""
import socket

with socket.create_connection(("127.0.0.1", 65432)) as connection:
    connection.sendall(b"Hello, world")
    print(f"Received {connection.recv(1024)!r}")
