import gpiod
import time

# Initialize GPIO chip (assuming gpiochip0)
chip = gpiod.Chip('gpiochip0')

# Set up TRIG and ECHO lines (GPIO26 for TRIG and GPIO27 for ECHO)
TRIG_LINE = chip.get_line(26)  # Trigger
ECHO_LINE = chip.get_line(25)  # Echo

# Request both lines for output/input
TRIG_LINE.request(consumer="Ultrasonic_TRIG", type=gpiod.LINE_REQ_DIR_OUT)
ECHO_LINE.request(consumer="Ultrasonic_ECHO", type=gpiod.LINE_REQ_DIR_IN)

def measure_distance():
    # Ensure the TRIG line is low before starting the measurement
    TRIG_LINE.set_value(0)
    time.sleep(0.002)  # Wait for 2 milliseconds to settle

    # Send a 10us pulse to TRIG to start measurement
    TRIG_LINE.set_value(1)
    time.sleep(0.00001)  # Delay for 10 microseconds
    TRIG_LINE.set_value(0)

    print("Trigger pulse sent.")

    # Wait for ECHO to go high (start pulse)
    pulse_start = None
    pulse_end = None
    timeout_start = time.time()

    # Wait for ECHO to go high (signal start)
    while ECHO_LINE.get_value() == 0:
        pulse_start = time.time()
        if pulse_start - timeout_start > 2:  # 2-second timeout
            print("Timeout: Echo signal didn't go high")
            return None

    print("Echo signal received, waiting for it to go low...")

    # Wait for ECHO to go low (signal end)
    timeout_start = time.time()
    while ECHO_LINE.get_value() == 1:
        pulse_end = time.time()
        if pulse_end - timeout_start > 2:  # 2-second timeout
            print("Timeout: Echo signal didn't go low")
            return None

    # Calculate the pulse duration
    pulse_duration = pulse_end - pulse_start
    print(f"Pulse duration: {pulse_duration} seconds")

    # Calculate distance (Speed of sound = 34300 cm/s in air)
    distance = pulse_duration * 17150  # Distance in centimeters

    return distance

try:
    while True:
        # Get the current distance measurement
        distance = measure_distance()
        if distance is not None:
            print(f"Distance: {distance:.2f} cm")
        else:
            print("Failed to measure distance.")
        
        # Wait 2 seconds before taking another measurement
        time.sleep(2)

except KeyboardInterrupt:
    print("Measurement stopped by User")
