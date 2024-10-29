import pyttsx3

engine = pyttsx3.init()

# List available voices
voices = engine.getProperty('voices')
uk_voice = None
for voice in voices:
    if "english" in voice.name.lower() and "uk" in voice.id.lower():
        uk_voice = voice
        break

if uk_voice:
    print("Using UK English voice:")
    print(" - ID: %s" % uk_voice.id)
    print(" - Name: %s" % uk_voice.name)
    engine.setProperty('voice', uk_voice.id)
else:
    print("UK English voice not found. Using default voice.")
    engine.setProperty('voice', voices[0].id)

# Set speaking rate to a more natural human-like speed
engine.setProperty('rate', 165)  # Adjust rate between 125-175 for natural sound

# William speaks with a UK English voice
engine.say()
engine.runAndWait()
