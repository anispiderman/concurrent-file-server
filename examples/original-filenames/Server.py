"""Compatibility entry point matching the original project filename."""
from pathlib import Path
from server import FileServer

if __name__ == "__main__":
    FileServer("127.0.0.1", 50000, Path("shared"), max_clients=3).serve()
