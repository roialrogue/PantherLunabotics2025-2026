import math
import pygame
import time
from pyrplidar import PyRPlidar

# -------------------------------
# Configuration
# -------------------------------
WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
MIN_DISTANCE = 50      # mm
MAX_DISTANCE = 3000    # mm
SCALE = (WIDTH // 2) / MAX_DISTANCE

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
    angle_rad = math.radians(angle_deg)
    r = distance_mm * SCALE
    x = CENTER[0] + int(r * math.cos(angle_rad))
    y = CENTER[1] - int(r * math.sin(angle_rad))  # y-axis inverted in pygame
    return x, y

# -------------------------------
# Main radar function
# -------------------------------
def radar_continuous_map():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RPLidar Radar Map")
    clock = pygame.time.Clock()

    font_small = pygame.font.SysFont(None, 20)
    font_title = pygame.font.SysFont(None, 28, bold=True)

    # Create a static surface for persistent map
    radar_surface = pygame.Surface((WIDTH, HEIGHT))
    radar_surface.fill(BLACK)

    # Draw reference circles ONCE
    for r in range(500, MAX_DISTANCE + 1, 500):
        pygame.draw.circle(radar_surface, DARK_GREEN, CENTER, int(r * SCALE), 1)
        label = font_small.render(f"{r//10} cm", True, WHITE)
        screen.blit(label, (CENTER[0] + int(r * SCALE) - 25, CENTER[1]))

    # -------------------------------
    # Connect to LIDAR
    # -------------------------------
    lidar = PyRPlidar()
    lidar.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)
    lidar.set_motor_pwm(500)
    time.sleep(2)  # let motor stabilize

    scan_generator = lidar.scan()  # returns multiple points per call

    points = []
    running = True
    try:
        for scan in scan_generator():
            # Handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Collect all points from this batch
            for measurement in scan:  # measurement has .angle, .distance
                angle, distance = measurement.angle, measurement.distance
                if MIN_DISTANCE <= distance <= MAX_DISTANCE:
                    points.append((angle, distance))

            # Draw points on radar_surface
            for ang, dist in points:
                px, py = polar_to_cartesian(ang, dist)
                if dist <= 1000:
                    color = RED
                elif dist <= 2000:
                    color = YELLOW
                else:
                    color = GREEN
                pygame.draw.circle(radar_surface, color, (px, py), 2)

            # Blit radar_surface to screen
            screen.blit(radar_surface, (0, 0))

            # Draw title
            title_surface = font_title.render("RPLidar Radar Map", True, WHITE)
            screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT - 40))

            pygame.display.flip()
            clock.tick(60)  # 60 FPS

            if not running:
                break

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        lidar.stop()
        lidar.set_motor_pwm(0)
        lidar.disconnect()
        pygame.quit()

# -------------------------------
# Entry point
# -------------------------------
if __name__ == "__main__":
    radar_continuous_map()