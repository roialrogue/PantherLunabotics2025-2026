# import os
# from math import cos, sin, pi, floor
# import pygame
# from adafruit_rplidar import RPLidar
# # Set up pygame and the display
# os.putenv('SDL_FBDEV', '/dev/fb1')
# pygame.init()
# lcd = pygame.display.set_mode((320,240))
# pygame.mouse.set_visible(False)
# lcd.fill((0,0,0))
# pygame.display.update()
# # Setup the RPLidar
# PORT_NAME = '/dev/ttyUSB0'
# lidar = RPLidar(None, PORT_NAME)
# # used to scale data to fit on the screen
# max_distance = 0

# def process_data(data):
#     global max_distance
#     lcd.fill((0,0,0))
#     for angle in range(360):
#         distance = data[angle]
#         if distance > 0: # ignore initially ungathered data points
#             max_distance = max([min([5000, distance]), max_distance])
#             radians = angle * pi / 180.0
#             x = distance * cos(radians)
#             y = distance * sin(radians)
#             point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance *
#             119))
#             lcd.set_at(point, pygame.Color(255, 255, 255))
#     pygame.display.update()

# scan_data = [0]*360

# try:
#     print(lidar.info)
#     for scan in lidar.iter_scans():
#         for (_, angle, distance) in scan:
#             scan_data[min([359, floor(angle)])] = distance
#         process_data(scan_data)
# except KeyboardInterrupt:
#     print('Stoping.')
# lidar.stop()
# lidar.disconnect()


import os
import time
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

scan_data = [0]*360

GRID_W = 80   # terminal width
GRID_H = 40   # terminal height
MAX_DIST = 4000  # max lidar distance to normalize

def draw_ascii_map(data):
    # Create blank ASCII grid
    grid = [[" " for _ in range(GRID_W)] for _ in range(GRID_H)]

    for angle in range(360):
        d = data[angle]
        if d > 0:
            # normalize distance [0..1]
            d_norm = min(d, MAX_DIST) / MAX_DIST   

            rad = angle * pi / 180
            x = d_norm * cos(rad)
            y = d_norm * sin(rad)

            # convert to grid coords
            gx = int((x + 1) * (GRID_W//2))
            gy = int((1 - y) * (GRID_H//2))

            if 0 <= gx < GRID_W and 0 <= gy < GRID_H:
                grid[gy][gx] = "#"

    # Clear terminal
    os.system("clear")

    # Print map
    for row in grid:
        print("".join(row))

try:
    print(lidar.info)
    time.sleep(2)   
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance

        draw_ascii_map(scan_data)

except KeyboardInterrupt:
    print('Stopping.')
    lidar.stop()
    lidar.disconnect()