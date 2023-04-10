import logging
from time import sleep

from pylgbst.hub import MoveHub
from pylgbst import get_connection_gatt
from pylgbst.peripherals import EncodedMotor, TiltSensor, Current, Voltage, COLORS, COLOR_BLACK

log = logging.getLogger("demo")


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
    conn = get_connection_gatt(hub_mac='00:16:53:AA:C3:4D')
    hub = MoveHub(conn)

    for device in hub.peripherals:
        print(device)

    demo_led_colors(hub)


if __name__ == '__main__':
    test_bluetooth_connection()
