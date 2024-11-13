import gpiod
import time

# Constants
SERVO_PIN_1 = 6  # First servo on GPIO pin 6
SERVO_PIN_2 = 5  # Second servo on GPIO pin 5
PWM_FREQUENCY = 50  # Standard PWM frequency for servos (50 Hz)
PERIOD_NS = int(1e9 / PWM_FREQUENCY)  # Period in nanoseconds (for 50Hz frequency)

# Pulse width for specific angles (in nanoseconds)
PULSE_WIDTH_0_DEGREE = int(1e6)  # 1 ms pulse width for 0 degrees //  ke kanan
PULSE_WIDTH_60_DEGREE = int(1.333333e6) 
PULSE_WIDTH_90_DEGREE = int(1.5e6)  # 1.5 ms pulse width for 90 degrees // lurus
PULSE_WIDTH_120_DEGREE = int(1.666e6)
PULSE_WIDTH_180_DEGREE = int(2e6)  # 2 ms pulse width for 180 degrees //  ke kiri

# Setup GPIOD
chip = gpiod.Chip('gpiochip4')
line_1 = chip.get_line(SERVO_PIN_1)
line_2 = chip.get_line(SERVO_PIN_2)

line_1.request(consumer="servo_control", type=gpiod.LINE_REQ_DIR_OUT)
line_2.request(consumer="servo_control", type=gpiod.LINE_REQ_DIR_OUT)

def set_servo_position(line, duty_cycle_ns):
    """ Set the servo position by changing the duty cycle """
    for _ in range(50):  # Apply signal 50 times to ensure movement
        line.set_value(1)
        time.sleep(duty_cycle_ns / 1e9)  # High for duty_cycle_ns
        line.set_value(0)
        time.sleep((PERIOD_NS - duty_cycle_ns) / 1e9)  # Low for remainder of the period

def move_servo_pin_1():
    """ Move servo on pin 2 to 90 and 180 degrees """
    set_servo_position(line_1, PULSE_WIDTH_120_DEGREE)
    time.sleep(1)
    set_servo_position(line_1, PULSE_WIDTH_90_DEGREE)
    time.sleep(1)
    set_servo_position(line_1, PULSE_WIDTH_60_DEGREE)
    time.sleep(1)

def move_servo_pin_2():
    """ Move servo on pin 2 to 90 and 180 degrees """
    set_servo_position(line_2, PULSE_WIDTH_0_DEGREE)
    time.sleep(1)
    set_servo_position(line_2, PULSE_WIDTH_90_DEGREE)
    time.sleep(1)
    set_servo_position(line_2, PULSE_WIDTH_180_DEGREE)
    time.sleep(1)

# Example usage:
move_servo_pin_1()  # Move servo 1 to 0 and then 180 degrees
# move_servo_pin_2()  # Move servo 2 to 90 and then 180 degrees
