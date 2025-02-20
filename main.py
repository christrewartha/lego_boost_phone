import logging
from time import sleep
import keyboard
from pylgbst.hub import MoveHub
from pylgbst import get_connection_gatt
from pylgbst import get_connection_bleak
from pylgbst.peripherals import EncodedMotor, TiltSensor, Current, Voltage, COLORS, COLOR_BLACK

import platform
import os
supported_platforms = ["Windows"]


def is_android():
    return platform.system() == 'Linux' and os.path.exists('/system/build.prop')

def get_platform():
    if is_android():
        return "Android"
    else:
        return platform.system()

def get_platform_info():
        return f"Running on {get_platform()}"

def is_platform_supported():
    return get_platform() in supported_platforms



log = logging.getLogger("demo")
current_move_state = "stop"

def demo_led_colors(movehub):
    # LED colors demo
    log.info("LED colors demo")

    # We get a response with payload and port, not x and y here...
    def colour_callback(named):
        log.info("LED Color callback: %s", named)

    movehub.led.subscribe(colour_callback)
    for color in list(COLORS.keys())[1:] + [COLOR_BLACK]:
        log.info("Setting LED color to: %s", COLORS[color])
        movehub.led.set_color(color)
        sleep(1)


def test_bluetooth_connection():
    conn = get_connection_bleak(hub_mac='00:16:53:AA:C3:4D')
    hub = MoveHub(conn)

    for device in hub.peripherals:
        print(device)

    demo_led_colors(hub)

def get_connection():
    hub_mac = '00:16:53:AA:C3:4D'
    if get_platform() == "Windows":
        conn = get_connection_bleak(hub_mac)
        connected_hub = MoveHub(conn)
        return connected_hub
    elif get_platform() == "Android":
        conn = get_connection_gatt(hub_mac)
        connected_hub = MoveHub(conn)
        return connected_hub
    else:
        return None


def user_control(movehub):
    import keyboard  # Make sure to install the keyboard library
    log.info("User control mode activated")

    move_speed = 0.5  # Define move speed
    turn_speed = 0.5   # Define turn speed

    global current_move_state

    if keyboard.is_pressed('w'):  # Move forward
        if current_move_state != "forward":
            log.info("Moving forward")
            movehub.motor_A.start_speed(move_speed)
            movehub.motor_B.start_speed(move_speed)
            current_move_state = "forward"
    elif keyboard.is_pressed('s'):  # Move backward
        if current_move_state != "backward":
            log.info("Moving backward")
            movehub.motor_A.start_speed(-move_speed)
            movehub.motor_B.start_speed(-move_speed)
            current_move_state = "backward"
    elif keyboard.is_pressed('a'):  # Turn left
        if current_move_state != "left":
            log.info("Turning left")
            movehub.motor_A.start_speed(-turn_speed)
            movehub.motor_B.start_speed(turn_speed)
            current_move_state = "left"
    elif keyboard.is_pressed('d'):  # Turn right
        if current_move_state != "right":
            log.info("Turning right")
            movehub.motor_A.start_speed(turn_speed)
            movehub.motor_B.start_speed(-turn_speed)
            current_move_state = "right"
    elif keyboard.is_pressed('x'):
        if current_move_state != "stop":
            log.info("Stopping")
            movehub.motor_A.stop()
            movehub.motor_B.stop()
            current_move_state = "stop"


if __name__ == '__main__':
    print(get_platform_info())
    if not is_platform_supported():
        print("This platform is not supported")
        exit(1)

    hub = get_connection()
    control_state = "user_control"  # Introduce control state

    while True:
        if control_state == "user_control":
            user_control(hub)
        elif keyboard.is_pressed('m'):  # Example key to switch modes
            log.info("Switching to another mode")
            control_state = "another_mode"  # Placeholder for another mode
            # Add logic for the new mode here
