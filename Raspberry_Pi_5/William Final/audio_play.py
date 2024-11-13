import pygame

# Initialize Pygame mixer
pygame.mixer.init()
pygame.mixer.music.load("/home/william/Desktop/Ultrasonic William-GPT/Whistle(1).mp3")

def play_audio():
    pygame.mixer.music.play()
    print("Audio is playing...")

def stop_audio():
    pygame.mixer.music.stop()
    print("Audio stopped.")

def is_audio_playing():
    return pygame.mixer.music.get_busy()
