import numpy as np
import warnings
import sounddevice as sd
import whisper

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

model = whisper.load_model("base")

def transcribe_audio(duration=2, fs=16000):
    print("Listening...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    audio = np.squeeze(recording)
    result = model.transcribe(audio)
    print(result['text'])
    return result['text']
