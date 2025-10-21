import pygame
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("❌ No joystick detected.")
    quit()

joy = pygame.joystick.Joystick(0)
joy.init()
print(f"✅ Detected joystick: {joy.get_name()}")
print(f"Buttons: {joy.get_numbuttons()}")

while True:
    pygame.event.pump()
    for i in range(joy.get_numbuttons()):
        if joy.get_button(i):
            print(f"Button {i} pressed!")
