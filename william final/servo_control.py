import time
import gpiod
import random
import threading

# Constants
SERVO_PIN_1 = 24
SERVO_PIN_2 = 23
PWM_FREQUENCY = 50
PERIOD_NS = int(1e9 / PWM_FREQUENCY)

# Pulse widths
PULSE_WIDTH_0_DEGREE = int(1e6)
PULSE_WIDTH_60_DEGREE = int(1.333333e6)
PULSE_WIDTH_90_DEGREE = int(1.5e6)
PULSE_WIDTH_120_DEGREE = int(1.666e6)
PULSE_WIDTH_180_DEGREE = int(2e6)

# Setup GPIOD
chip = gpiod.Chip('gpiochip4')
line_1 = chip.get_line(SERVO_PIN_1)
line_2 = chip.get_line(SERVO_PIN_2)

line_1.request(consumer="servo_control", type=gpiod.LINE_REQ_DIR_OUT)
line_2.request(consumer="servo_control", type=gpiod.LINE_REQ_DIR_OUT)

def stop_servo(line):
    line.set_value(0)

def set_servo_position(line, duty_cycle_ns):
    for _ in range(50):
        line.set_value(1)
        time.sleep(duty_cycle_ns / 1e9)
        line.set_value(0)
        time.sleep((PERIOD_NS - duty_cycle_ns) / 1e9)

def move_servo_pin_1():
    set_servo_position(line_1, PULSE_WIDTH_120_DEGREE)
    time.sleep(0.5)
    set_servo_position(line_1, PULSE_WIDTH_90_DEGREE)
    time.sleep(0.5)
    set_servo_position(line_1, PULSE_WIDTH_60_DEGREE)
    time.sleep(0.5)

def move_servo_pin_2():
    set_servo_position(line_2, PULSE_WIDTH_120_DEGREE)
    time.sleep(0.5)
    set_servo_position(line_2, PULSE_WIDTH_90_DEGREE)
    time.sleep(0.5)
    set_servo_position(line_2, PULSE_WIDTH_60_DEGREE)
    time.sleep(0.5)

def move_servos_randomly():
    actions = [move_servo_pin_1, move_servo_pin_2]
    random.choice(actions)()

def move_servos_during_speech(stop_event):
    while not stop_event.is_set():
        move_servos_randomly()
        time.sleep(0.5)  # Adjust the speed of movements

def release_servo_lines():
    line_1.release()
    line_2.release()
