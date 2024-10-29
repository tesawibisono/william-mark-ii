import time
import gpiod

chip = gpiod.Chip('gpiochip4')
TRIG_LINE = chip.get_line(26)
ECHO_LINE = chip.get_line(25)

TRIG_LINE.request(consumer="Ultrasonic", type=gpiod.LINE_REQ_DIR_OUT)
ECHO_LINE.request(consumer="Ultrasonic", type=gpiod.LINE_REQ_DIR_IN)

def get_distance():
    TRIG_LINE.set_value(1)
    time.sleep(0.00001)
    TRIG_LINE.set_value(0)

    pulse_start = pulse_end = time.time()
    while ECHO_LINE.get_value() == 0:
        pulse_start = time.time()

    while ECHO_LINE.get_value() == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

def release_ultrasonic_lines():
    TRIG_LINE.release()
    ECHO_LINE.release()
