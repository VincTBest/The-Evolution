import pygame


def get_controller_type():
    if pygame.joystick.get_count() == 0:
        return "No controller connected"

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    controller_name = joystick.get_name().lower()

    if "dualsense" in controller_name:
        return "ps5"

    if "dualshock" in controller_name:
        return "ps4"

    if "xbox" in controller_name:
        return "x"

    if "amazon" in controller_name and "luna" in controller_name:
        return "al"

    # Check for PS5 triggers (L2 and R2 are axes 2 and 5)
    trigger_axes = [2, 5]  # L2, R2 are axes 2 and 5 for PS5
    for axis in trigger_axes:
        if abs(joystick.get_axis(axis)) > 0.1:  # If the axis values are non-zero (indicating trigger is pressed)
            return "ps5"

    # Check for Xbox triggers (buttons 6 and 7 for LT/RT)
    for i in range(joystick.get_numbuttons()):
        if i == 6 or i == 7:  # Xbox-like controllers use LT/RT (buttons 6 and 7)
            if joystick.get_button(i):
                return "x"

    return "unk"
