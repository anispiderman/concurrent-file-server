from __future__ import annotations

import argparse
import json
import socket
import struct
import threading
from pathlib import Path

MAX_FRAME = 64 * 1024


def send_frame(sock: socket.socket, payload: bytes) -> None:
    sock.sendall(struct.pack("!I", len(payload)) + payload)


def recv_exact(sock: socket.socket, size: int) -> bytes:
    chunks = bytearray()
    while len(chunks) < size:
        chunk = sock.recv(size - len(chunks))
        if not chunk:
            raise ConnectionError("peer disconnected")
        chunks.extend(chunk)
    return bytes(chunks)


def recv_frame(sock: socket.socket) -> bytes:
    size = struct.unpack("!I", recv_exact(sock, 4))[0]
    if size > MAX_FRAME:
        raise ValueError("frame exceeds limit")
    return recv_exact(sock, size)


class FileServer:
    def __init__(self, host: str, port: int, root: Path, max_clients: int = 8):
        self.address = (host, port)
        self.root = root.resolve()
        self.slots = threading.BoundedSemaphore(max_clients)

    def resolve_name(self, name: str) -> Path:
        candidate = (self.root / name).resolve()
        if candidate.parent != self.root:
            raise ValueError("nested paths are not allowed")
        return candidate

    def handle(self, conn: socket.socket) -> None:
        with conn, self.slots:
            while True:
                try:
                    request = json.loads(recv_frame(conn))
                    command = request.get("command")
                    if command == "list":
                        files = sorted(p.name for p in self.root.iterdir() if p.is_file())
                        send_frame(conn, json.dumps({"ok": True, "files": files}).encode())
                    elif command == "get":
                        path = self.resolve_name(str(request.get("name", "")))
                        if not path.is_file():
                            send_frame(conn, json.dumps({"ok": False, "error": "not found"}).encode())
                        else:
                            data = path.read_bytes()
                            send_frame(conn, json.dumps({"ok": True, "size": len(data)}).encode())
                            send_frame(conn, data)
                    elif command == "quit":
                        send_frame(conn, json.dumps({"ok": True}).encode())
                        return
                    else:
                        send_frame(conn, json.dumps({"ok": False, "error": "unknown command"}).encode())
                except (ConnectionError, json.JSONDecodeError):
                    return
                except (OSError, ValueError) as exc:
                    send_frame(conn, json.dumps({"ok": False, "error": str(exc)}).encode())

    def serve(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        with socket.create_server(self.address, reuse_port=False) as listener:
            print(f"Serving {self.root} on {listener.getsockname()}")
            while True:
                conn, _ = listener.accept()
                threading.Thread(target=self.handle, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=50000)
    parser.add_argument("--root", type=Path, default=Path("shared"))
    args = parser.parse_args()
    FileServer(args.host, args.port, args.root).serve()
