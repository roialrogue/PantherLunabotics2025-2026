"""
Lidar stream viewer — run this on your laptop.
Connects to the Pi and displays the radar feed in a local pygame window.

Usage:
    python mission_control/lidar_viewer.py <pi-ip-address>
    python mission_control/lidar_viewer.py 192.168.1.42
"""

import argparse
import io
import socket
import struct
import sys

import pygame
from PIL import Image

STREAM_PORT = 5000
WIDTH, HEIGHT = 800, 800


def recv_exact(sock, n):
    """Read exactly n bytes from sock, or raise ConnectionError."""
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Connection closed by server")
        data += chunk
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='IP address of the Raspberry Pi')
    parser.add_argument('--port', type=int, default=STREAM_PORT)
    args = parser.parse_args()

    print(f"Connecting to {args.host}:{args.port}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.host, args.port))
    print("Connected. Receiving stream...")

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RPLidar Remote View")
    clock = pygame.time.Clock()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # Read 4-byte length header, then the JPEG frame
            header = recv_exact(sock, 4)
            frame_len = struct.unpack('>I', header)[0]
            frame_bytes = recv_exact(sock, frame_len)

            img = Image.open(io.BytesIO(frame_bytes)).convert('RGB')
            mode = img.mode
            size = img.size
            data = img.tobytes()
            surface = pygame.image.fromstring(data, size, mode)
            screen.blit(surface, (0, 0))
            pygame.display.flip()
            clock.tick(60)

    except (ConnectionError, KeyboardInterrupt):
        print("\nDisconnected.")
    finally:
        sock.close()
        pygame.quit()


if __name__ == "__main__":
    main()
