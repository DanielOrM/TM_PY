"""Transition de type fondu"""
import tkinter as tk
import pygame


class FadeTransition(tk.Label):
    """
    Transition de type fondu
        - bruits de pas début + stop
        - blanc --> noir (flash)
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(background="gray")
        label_background_system_color = self.cget("background")
        label_background_16_bit_color = self.winfo_rgb(label_background_system_color)
        label_background_8_bit_color = tuple(value >> 8 for value in label_background_16_bit_color)
        self.start_color = label_background_8_bit_color     # blanc
        self.end_color = tuple((0, 0, 0))   # noir
        # lapse de temps
        self.duration_ms = 1000
        self.frames_per_second = 60
        self.ms_sleep_duration = 1000 // self.frames_per_second
        self.current_step = 0
        self.fade_transition_ended = False
        # self.create_transition()
        # self.new_color = None

    def create_transition(self):
        """
        Transition en plein écran
        Bruits de pas enclenché
        Lancement transition
        """
        self.grid(row=0, column=0, sticky="NSWE")
        # bruits de pas
        pygame.mixer.music.load("./son/bruits-pas-son.mp3")
        pygame.mixer.music.play(loops=0)
        self.update_label()

    def interpolate(self, color_a, color_b, t):
        """
        Return tuple avec couleurs (blanc--> noir) qui changent
        """
        # 'color_a' et 'color_b' sont des tuples RGB
        # 't' = valeur entre 0.0 et 1.0
        return tuple(int(a + (b - a) * t) for a, b in zip(color_a, color_b))

    def update_label(self):
        """
        Changement blanc --> noir progressif (t)
        Quand transition stop --> fin bruits de pas
        """
        t = (1.0 / self.frames_per_second) * self.current_step
        self.current_step += 0.7
        # print(self.current_step)
        new_color = self.interpolate(self.start_color, self.end_color, t)
        # print(self.new_color)
        self.configure(background="#%02x%02x%02x" % new_color)
        if self.current_step <= self.frames_per_second:
            self.after(self.ms_sleep_duration, self.update_label)
        else:
            # self.pack_forget()
            self.current_step = 0
            self.grid_remove()
            self.fade_transition_ended = True
            if self.fade_transition_ended:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                self.master.check_game_events()
                self.fade_transition_ended = False
