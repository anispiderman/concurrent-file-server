# Concurrent File Server

A dependency-free Python TCP client/server that serves multiple clients concurrently using one thread per connection and a length-prefixed binary protocol.

## Features

- bounded concurrent-client handling
- deterministic JSON control messages and binary-safe file transfer
- path-traversal protection and maximum frame size
- graceful client disconnects
- protocol unit tests

## Run

```sh
python3 server.py --root shared
python3 client.py
```

## Test

```sh
python3 -m unittest discover -s tests -v
```

This is a clean portfolio edition based on concepts explored in a completed networking project. It does not reuse the shared repository's history and does not claim other contributors' work.
