from __future__ import annotations

import argparse
import json
import socket
from pathlib import Path
from server import recv_frame, send_frame

def request(sock: socket.socket, command: str, **values: str) -> dict:
    send_frame(sock, json.dumps({"command": command, **values}).encode())
    return json.loads(recv_frame(sock))

def main(host: str, port: int) -> None:
    with socket.create_connection((host, port)) as sock:
        while True:
            action = input("command [list/get/quit]: ").strip().lower()
            if action == "list":
                print(request(sock, "list"))
            elif action == "get":
                name = input("file name: ").strip()
                response = request(sock, "get", name=name)
                if response.get("ok"):
                    output_name = Path(name).name
                    Path(output_name).write_bytes(recv_frame(sock))
                    print(f"saved {output_name} ({response['size']} bytes)")
                else:
                    print(response["error"])
            elif action == "quit":
                request(sock, "quit")
                return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=50000)
    args = parser.parse_args()
    main(args.host, args.port)
