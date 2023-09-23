"""Sons randoms dès que pièces visibles"""
import threading
import pygame
from random import randrange
from os import listdir
from os.path import isfile, join
from son.channels import sound_effects_channel

SOUND_PATH = "./son/effets/"
SOUND_EFFECTS = [f for f in listdir(SOUND_PATH) if isfile(join(SOUND_PATH, f))]
# print(SOUND_EFFECTS)


def play_sound_effect():
    """
    Joue un son de manière "random" dans une liste d'effets sonores
    """
    print("SON RANDOM")
    index = randrange(len(SOUND_EFFECTS)-1)
    randm_effect_path = SOUND_PATH+SOUND_EFFECTS[index]
    randm_effect = pygame.mixer.Sound(randm_effect_path)
    sound_effects_channel.play(randm_effect)
    # pygame.mixer.music.load(f"{SOUND_PATH+SOUND_EFFECTS[index]}")
    # pygame.mixer.music.play()


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t
