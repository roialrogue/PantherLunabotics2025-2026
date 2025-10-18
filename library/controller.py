import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)  # Get the first joystick
    joystick.init()
    print(f"Detected joystick: {joystick.get_name()}")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed")
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis ==2:
                    print(f"Axis {event.axis} moved to {event.value}")
else:
    print("No joystick detected.")

pygame.quit()