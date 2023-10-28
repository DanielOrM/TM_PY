"""Tous les channels utilisés"""
import pygame

pygame.mixer.init()
pygame.mixer.set_num_channels(8)
music = pygame.mixer.Channel(0)
sound_effects_channel = pygame.mixer.Channel(1)
pen_channel = pygame.mixer.Channel(2)
walk_sound_channel = pygame.mixer.Channel(3)
monster_music = pygame.mixer.Channel(4)
