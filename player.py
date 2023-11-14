import pygame
from pygame import mixer

pygame.init()
mixer.init()

mixer.music.load("E:\py_project\ChatCLM+genshinTTS\\audio\\tmp.wav")
mixer.music.play()

while mixer.music.get_busy():
    pygame.time.Clock().tick(10)