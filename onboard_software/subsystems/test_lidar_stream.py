import argparse
import io
import math
import os
import socket
import struct
import time

# pygame import is deferred so we can set SDL env vars first
from rplidar import RPLidar

# -------------------------------
# Configuration
# -------------------------------
WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
MIN_DISTANCE = 50      # mm
MAX_DISTANCE = 3000    # mm
SCALE = (WIDTH // 2) / MAX_DISTANCE
STREAM_PORT = 5000

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 100, 0)
WHITE = (255, 255, 255)

# -------------------------------
# Helper function
# -------------------------------
def polar_to_cartesian(angle_deg, distance_mm):
    angle_rad = math.radians((angle_deg + 180) % 360)
    r = distance_mm * SCALE
    x = CENTER[0] + int(r * math.cos(angle_rad))
    y = CENTER[1] + int(r * math.sin(angle_rad))
    return x, y

# -------------------------------
# Frame encoding
# -------------------------------
def encode_frame(surface):
    """Encode a pygame surface as JPEG bytes."""
    from PIL import Image
    arr = pygame.surfarray.array3d(surface)
    arr = arr.transpose(1, 0, 2)  # (w,h,3) -> (h,w,3) for PIL
    img = Image.fromarray(arr, 'RGB')
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=70)
    return buf.getvalue()

def send_frame(conn, frame_bytes):
    """Send a length-prefixed frame over a socket."""
    header = struct.pack('>I', len(frame_bytes))
    conn.sendall(header + frame_bytes)

# -------------------------------
# Main radar function
# -------------------------------
def radar_map(stream=False):
    global pygame

    if stream:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'

    import pygame as _pygame
    pygame = _pygame

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    if not stream:
        pygame.display.set_caption("RPLidar Radar Map")
    clock = pygame.time.Clock()
    font_small = pygame.font.SysFont(None, 20)
    font_title = pygame.font.SysFont(None, 28, bold=True)

    radar_surface = pygame.Surface((WIDTH, HEIGHT))
    radar_surface.fill(BLACK)

    # -------------------------------
    # Set up streaming socket (if --stream)
    # -------------------------------
    conn = None
    if stream:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(('0.0.0.0', STREAM_PORT))
        server_sock.listen(1)
        print(f"Streaming server listening on port {STREAM_PORT} — waiting for viewer to connect...")
        conn, addr = server_sock.accept()
        print(f"Viewer connected from {addr}")

    # -------------------------------
    # Connect to LIDAR
    # -------------------------------
    PORT_NAME = '/dev/ttyUSB0'
    lidar = RPLidar(PORT_NAME)
    time.sleep(2)  # let motor stabilize

    running = True
    try:
        for scan in lidar.iter_scans():
            if not stream:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

            # Clear the radar surface each frame
            radar_surface.fill(BLACK)

            # Draw reference circles
            for r in range(500, MAX_DISTANCE + 1, 500):
                pygame.draw.circle(radar_surface, DARK_GREEN, CENTER, int(r * SCALE), 1)
                label = font_small.render(f"{r//10} cm", True, WHITE)
                radar_surface.blit(label, (CENTER[0] + int(r * SCALE) - 25, CENTER[1]))

            # Draw scan points
            for (quality, angle, distance) in scan:
                if MIN_DISTANCE <= distance <= MAX_DISTANCE:
                    px, py = polar_to_cartesian(angle, distance)
                    if distance <= 1000:
                        color = RED
                    elif distance <= 2000:
                        color = YELLOW
                    else:
                        color = GREEN
                    pygame.draw.circle(radar_surface, color, (px, py), 2)

            screen.blit(radar_surface, (0, 0))
            title_surface = font_title.render("RPLidar Radar Map", True, WHITE)
            screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT - 40))

            if stream:
                try:
                    send_frame(conn, encode_frame(screen))
                except (BrokenPipeError, ConnectionResetError):
                    print("Viewer disconnected.")
                    break
            else:
                pygame.display.flip()
                clock.tick(60)

            if not running:
                break

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        pygame.quit()
        if conn:
            conn.close()
        if stream:
            server_sock.close()

# -------------------------------
# Entry point
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--stream', action='store_true',
                        help='Stream frames over TCP instead of displaying locally')
    args = parser.parse_args()
    radar_map(stream=args.stream)
