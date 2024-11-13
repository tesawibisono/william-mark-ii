import whisper
import pyttsx3
import sounddevice as sd
import numpy as np
import warnings

# Suppress the specific warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Load a smaller Whisper model
model = whisper.load_model("tiny")  # Use "tiny" for faster processing

# Initialize TTS engine
engine = pyttsx3.init()

# Function to record audio and transcribe with Whisper
def transcribe_audio():
    print("Listening...")
    duration = 2  # seconds (reduce duration for faster processing)
    fs = 16000  # Sample rate
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished

    # Convert the NumPy array to bytes and then to Whisper's expected format
    audio = np.squeeze(recording)
    result = model.transcribe(audio)
    return result['text']

# Main loop
try:
    while True:
        text = transcribe_audio()
        print(f"You said: {text}")

        # Use TTS to speak the text
        engine.say(text)
        engine.runAndWait()

except KeyboardInterrupt:
    print("Exiting...")
