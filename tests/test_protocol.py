import socket
import unittest

from server import recv_frame, send_frame


class ProtocolTests(unittest.TestCase):
    def test_binary_frame_round_trip(self):
        left, right = socket.socketpair()
        with left, right:
            payload = bytes(range(256))
            send_frame(left, payload)
            self.assertEqual(recv_frame(right), payload)

    def test_rejects_large_frame(self):
        left, right = socket.socketpair()
        with left, right:
            left.sendall((70_000).to_bytes(4, "big"))
            with self.assertRaises(ValueError):
                recv_frame(right)


if __name__ == "__main__":
    unittest.main()
