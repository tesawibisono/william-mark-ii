import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')
uk_voice = None
for voice in voices:
    if "english" in voice.name.lower() and "uk" in voice.id.lower():
        uk_voice = voice
        break

if uk_voice:
    print("Using UK English voice:")
    print(f" - ID: {uk_voice.id}")
    print(f" - Name: {uk_voice.name}")
    engine.setProperty('voice', uk_voice.id)
else:
    print("UK English voice not found. Using default voice.")
    engine.setProperty('voice', voices[0].id)

engine.setProperty('rate', 165)

speaking = False

def speak(text):
    global speaking
    speaking = True
    engine.say(text)
    engine.runAndWait()
    speaking = False

def is_speaking():
    return speaking
