import time
import gpiod

# Constants
SERVO_PIN_1 = 24  # Line number within gpiochip0
SERVO_PIN_2 = 23
PWM_FREQUENCY = 50
PERIOD_NS = int(1e9 / PWM_FREQUENCY)

# Pulse widths for different angles
PULSE_WIDTH_0_DEGREE = int(1e6)         # 1 ms pulse
PULSE_WIDTH_60_DEGREE = int(1.333e6)    # 1.333 ms pulse
PULSE_WIDTH_90_DEGREE = int(1.5e6)      # 1.5 ms pulse
PULSE_WIDTH_120_DEGREE = int(1.666e6)   # 1.666 ms pulse
PULSE_WIDTH_180_DEGREE = int(2e6)       # 2 ms pulse


# Setup GPIOD
chip = gpiod.Chip('gpiochip0')  # Changed from 'gpiochip4' to 'gpiochip0'
line_1 = chip.get_line(SERVO_PIN_1)
line_2 = chip.get_line(SERVO_PIN_2)

line_1.request(consumer="servo_control", type=gpiod.LINE_REQ_DIR_OUT)
line_2.request(consumer="servo_control", type=gpiod.LINE_REQ_DIR_OUT)

def set_servo_position(line, duty_cycle_ns):
    """
    Set the servo position by sending PWM signals.

    Args:
        line: The GPIO line connected to the servo.
        duty_cycle_ns: The pulse width in nanoseconds corresponding to the desired angle.
    """
    for _ in range(50):  # Send the pulse 50 times (approx 1 second at 50Hz)
        line.set_value(1)
        time.sleep(duty_cycle_ns / 1e9)
        line.set_value(0)
        time.sleep((PERIOD_NS - duty_cycle_ns) / 1e9)

def move_servo_to_positions(line, positions):
    """
    Move the servo through a list of positions.

    Args:
        line: The GPIO line connected to the servo.
        positions: A list of pulse widths representing different angles.
    """
    for position in positions:
        print(f"Moving servo on GPIO pin {line.offset()} to position with pulse width {position} ns")
        set_servo_position(line, position)
        time.sleep(0.5)

def move_servo_pin_1():
    positions = [
        PULSE_WIDTH_0_DEGREE,
        PULSE_WIDTH_60_DEGREE,
        PULSE_WIDTH_90_DEGREE,
        PULSE_WIDTH_120_DEGREE,
        PULSE_WIDTH_180_DEGREE
    ]
    move_servo_to_positions(line_1, positions)

def move_servo_pin_2():
    positions = [
        PULSE_WIDTH_0_DEGREE,
        PULSE_WIDTH_60_DEGREE,
        PULSE_WIDTH_90_DEGREE,
        PULSE_WIDTH_120_DEGREE,
        PULSE_WIDTH_180_DEGREE
    ]
    move_servo_to_positions(line_2, positions)

def reset_servo_position(line):
    """
    Reset the servo to the default position (90 degrees).

    Args:
        line: The GPIO line connected to the servo.
    """
    print(f"Resetting servo on GPIO pin {line.offset()} to 90 degrees.")
    set_servo_position(line, PULSE_WIDTH_60_DEGREE)

def release_servo_lines():
    line_1.release()
    line_2.release()

if __name__ == "__main__":
    try:
        print("Starting servo test on both pins.")
        print("Testing servo on pin 1...")
        move_servo_pin_1()
        print("Testing servo on pin 2...")
        move_servo_pin_2()
    except KeyboardInterrupt:
        print("Test interrupted by user.")
    finally:
        # Reset servo positions before releasing
        print("Resetting servos to default positions.")
        reset_servo_position(line_1)
        reset_servo_position(line_2)
        release_servo_lines()
        print("Servo test completed. GPIO lines have been released.")