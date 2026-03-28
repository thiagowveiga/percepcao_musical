import pygame
import os

notes_sounds = {}

def load_sounds(path: str) -> None:

    global notes_sounds
    pygame.mixer.init()
    for file_name in os.listdir(path):

        if file_name.endswith('.wav'):
            note = file_name.split('-')[-1].replace('.wav', '')
            sound = pygame.mixer.Sound(os.path.join(path, file_name))

            notes_sounds[note] = sound

def play(note: str) -> None:
    global notes_sounds
    if note in notes_sounds:
        notes_sounds[note].play()

def wait(ms: int) -> None:
    pygame.time.wait(ms)