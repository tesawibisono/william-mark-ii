import openai
import gpiod
import time
import random

# Read the API key from the file
with open("api_key.txt", "r") as file:
    openai.api_key = file.read().strip()

# Set up gpiod for Raspberry Pi 5
chip = gpiod.Chip('gpiochip4')  # Use the correct GPIO chip
TRIG_LINE = chip.get_line(26)   # Corresponds to GPIO 26
ECHO_LINE = chip.get_line(25)   # Corresponds to GPIO 25

# Configure the lines
TRIG_LINE.request(consumer="Ultrasonic", type=gpiod.LINE_REQ_DIR_OUT)
ECHO_LINE.request(consumer="Ultrasonic", type=gpiod.LINE_REQ_DIR_IN)

# Define a function to measure distance
def get_distance():
    # Trigger the sensor
    TRIG_LINE.set_value(1)
    time.sleep(0.00001)
    TRIG_LINE.set_value(0)

    # Wait for the echo
    pulse_start = pulse_end = time.time()
    while ECHO_LINE.get_value() == 0:
        pulse_start = time.time()

    while ECHO_LINE.get_value() == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

# Simulate head movement (nodding or shaking) and optionally whistle
def move_head_and_whistle():
    action = random.choice(["nod", "shake", "whistle", "both"])
    if action == "nod":
        print("William nods his head.")
    elif action == "shake":
        print("William shakes his head.")
    elif action == "whistle":
        whistle()
    elif action == "both":
        print("William shakes his head and whistles.")
        whistle()

# Simulate a whistle
def whistle():
    print("William whistles cheerfully.")

# Initialize conversation history
conversation_history = [
    {"role": "system", "content": "You are William, a friendly and supportive robot from the future. Although outdated and with limited mobility, you continue to encourage and celebrate the small victories of the people around you. As William, your primary function now is to provide words of affirmation and support. Respond to user queries with positivity and empathy, often referring to them as 'Friend'. Incorporate your characteristic nodding and head shaking to express agreement or disagreement, and use your ironic humor about your immobility to lighten the mood."}
]

# Define the talking distance range in centimeters
min_distance = 15
max_distance = 70

# Start the main loop
last_in_range_time = time.time()

try:
    while True:
        distance = get_distance()
        print(f"Measured Distance: {distance} cm")

        current_time = time.time()

        if min_distance <= distance <= max_distance:
            # Reset the timer if the user is back in range
            last_in_range_time = current_time

            # Get user input
            user_input = input("You: ")

            # Add user message to the conversation history
            conversation_history.append({"role": "user", "content": user_input})
            
            client = openai.OpenAI(api_key=openai.api_key)
                        
            response =client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation_history
            )

            # Extract and print the response
            response_text = response.choices[0].message.content.strip()
            print(f"William: {response_text}")

            # Add the assistant's response to the conversation history
            conversation_history.append({"role": "assistant", "content": response_text})
        
        elif current_time - last_in_range_time > 5:
            print("William: Hmm... Where did you go, Friend?")
            # William looks around (simulated by head movement and whistle)
            move_head_and_whistle()

            if current_time - last_in_range_time > 8:
                # After 3 more seconds, either move its head or whistle or both
                move_head_and_whistle()
                # Reset the timer to avoid repeated actions
                last_in_range_time = current_time

        else:
            # If the person is out of range and the last message was from the user
            if conversation_history[-1]["role"] == "user":
                print("William: Oh goodbye then!")
                # Add a final goodbye message to conversation history to end properly
                conversation_history.append({"role": "assistant", "content": "Oh goodbye then!"})
                break

        # Add a small delay to avoid spamming the sensor
        time.sleep(1)

finally:
    # Release the lines
    TRIG_LINE.release()
    ECHO_LINE.release()
