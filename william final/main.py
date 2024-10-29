import openai
import time
import random
import threading

from audio_play import play_audio, stop_audio, is_audio_playing
from servo_control import (
    move_servo_pin_1, move_servo_pin_2, move_servos_randomly,
    set_servo_position, stop_servo, PULSE_WIDTH_90_DEGREE, line_1, line_2,
    release_servo_lines, move_servos_during_speech
)
from speech_recognition import transcribe_audio
from tts_engine import speak, is_speaking
from ultrasonic_sensor import get_distance, release_ultrasonic_lines

# Read the API key from the file
with open("/home/william/Desktop/Ultrasonic William-GPT/api_key.txt", "r") as file:
    openai.api_key = file.read().strip()

# Initialize conversation history
conversation_history = [
    {"role": "system", "content": "You are William, a friendly robot from the future. As William, you often reffer to everyone as 'Friend'. Your only mobility is moving your head and neck."}
]

# Define the talking distance range in centimeters
min_distance = 15
max_distance = 70

last_in_range_time = time.time()
last_spoken_time = 0  # Time when William last said "Hmm... Where did you go, Friend?"
last_movement_time = 0  # Time when William last performed move_head_and_whistle()

# Use a reentrant lock to prevent deadlocks
action_lock = threading.RLock()

def move_head_and_whistle():
    with action_lock:
        try:
            if is_audio_playing() or is_speaking():
                # Don't proceed if audio or TTS is playing
                return
            action = random.choice(["nod", "shake", "both"])
            if action == "nod":
                print("William nods his head.")
                move_servo_pin_1()
            elif action == "shake":
                print("William shakes his head.")
                move_servo_pin_2()
            elif action == "both":
                print("William shakes his head and whistles.")
                servo_thread = threading.Thread(target=move_servos_randomly)
                servo_thread.start()
                time.sleep(1)
                whistle()
        except Exception as e:
            print(f"Exception in move_head_and_whistle: {e}")

def whistle():
    with action_lock:
        try:
            if is_audio_playing() or is_speaking():
                return
            print("William whistles cheerfully.")
            play_audio()
        except Exception as e:
            print(f"Exception in whistle: {e}")

try:
    while True:
        distance = get_distance()
        print(f"Measured Distance: {distance} cm")

        current_time = time.time()
        time_since_last_in_range = current_time - last_in_range_time
        time_since_last_spoken = current_time - last_spoken_time
        time_since_last_movement = current_time - last_movement_time

        if min_distance <= distance <= max_distance:
            # Person is in range
            with action_lock:
                last_in_range_time = current_time

                # Reset last spoken and movement times
                last_spoken_time = 0
                last_movement_time = 0

                # Stop any ongoing audio or servo movements
                stop_audio()
                set_servo_position(line_1, PULSE_WIDTH_90_DEGREE)
                set_servo_position(line_2, PULSE_WIDTH_90_DEGREE)
                stop_servo(line_1)
                stop_servo(line_2)

                # Transcribe user's speech
                vttext = transcribe_audio()
                conversation_history.append({"role": "user", "content": vttext})
                
                if(vttext == " Good bye."):
                    exit()

                client = openai.OpenAI(api_key=openai.api_key)

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=conversation_history
                )

                response_text = response.choices[0].message.content.strip()
                print(f"William: {response_text}")

                # Start servo movements during speech
                servo_stop_event = threading.Event()
                servo_thread = threading.Thread(target=move_servos_during_speech, args=(servo_stop_event,))
                servo_thread.start()

                # Speak the response
                speak(response_text)

                # Stop servo movements after speech
                servo_stop_event.set()
                servo_thread.join()

                conversation_history.append({"role": "assistant", "content": response_text})

        else:
            # Person is out of range
            time_since_last_in_range = current_time - last_in_range_time
            time_since_last_spoken = current_time - last_spoken_time
            time_since_last_movement = current_time - last_movement_time

            # After 5 seconds, say "Hmm... Where did you go, Friend?" once
            if time_since_last_in_range > 5 and last_spoken_time == 0:
                with action_lock:
                    if not is_audio_playing() and not is_speaking():
                        print("William: Hmm... Where did you go, Friend?")
                        speak("Hmm... Where did you go, Friend")
                        last_spoken_time = current_time  # Set last spoken time

            # After 10 seconds, perform move_head_and_whistle every 10 seconds
            if time_since_last_in_range > 10 and time_since_last_movement > 10:
                with action_lock:
                    if not is_audio_playing() and not is_speaking():
                        move_head_and_whistle()
                        last_movement_time = current_time  # Update last movement time

        # Sleep briefly to avoid busy-waiting
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    release_ultrasonic_lines()
    release_servo_lines()
