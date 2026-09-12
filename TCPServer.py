"""Minimal single-client uppercase-response TCP example."""
import socket

def start_server(host="127.0.0.1", port=12345):
    with socket.create_server((host, port)) as listener:
        connection, _ = listener.accept()
        with connection:
            data = connection.recv(1024)
            if data:
                connection.sendall(data.upper())

if __name__ == "__main__":
    start_server()
