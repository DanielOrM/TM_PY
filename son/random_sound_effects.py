"""Sons randoms dès que pièces visibles"""
import threading
import pygame
from random import randrange
from os import listdir
from os.path import isfile, join
from son.channels import sound_effects_channel

SOUND_PATH = "./son/effets/"
SOUND_EFFECTS = [f for f in listdir(SOUND_PATH) if isfile(join(SOUND_PATH, f))]


def play_sound_effect():
    """
    Joue un son de manière "random" dans une liste d'effets sonores
    """
    print("SON RANDOM")
    index = randrange(len(SOUND_EFFECTS))
    randm_effect_path = SOUND_PATH+SOUND_EFFECTS[index]
    randm_effect = pygame.mixer.Sound(randm_effect_path)
    sound_effects_channel.play(randm_effect)


class SetInterval:
    def __init__(self, func, sec):
        self.func = func
        self.sec = sec
        self.t = threading.Timer(self.sec, self.timer_manager)
        self.t.start()  # interval commence avec delay de X sec

    def timer_manager(self):
        self.t = threading.Timer(self.sec, self.timer_manager)
        self.t.start()
        self.func()

    def cancel(self):
        self.t.cancel()
