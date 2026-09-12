"""Client for TCPServer.py."""
import socket

def start_client(host="127.0.0.1", port=12345):
    with socket.create_connection((host, port)) as connection:
        connection.sendall(input("Message: ").encode())
        print(connection.recv(1024).decode())

if __name__ == "__main__":
    start_client()
