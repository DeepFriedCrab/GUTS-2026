import json
import socket
import uuid

# Constants
GAME_NAME = "2 FIGHT"
DISCOVERY_PORT = 241557
TCP_PORT = 241558
INTERVAL = 1.0

class Network:
    def __init__(self):
        self.id = uuid.uuid4()
        self.connected = None
        self.peer_addr = None
        self.buffer = b""
        self.last_broadcast = 0

        # tcp server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("", TCP_PORT))
        self.tcp_port = self.tcp_port

        self.server.listen(1)
        self.server.setblocking(False)

        # udp
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udp.bind(("", DISCOVERY_PORT))
        self.udp.setblocking(False)

    def close(self):
        self.server.close()
        self.udp.close()