"""Transition de type fondu"""
import tkinter as tk
import pygame
from PIL import ImageTk, Image

from global_var import screen_width, screen_height
from son.channels import walk_sound_channel


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
        self.is_walk_transition = False
        # self.create_transition()
        # self.new_color = None

    def create_transition(self, walk=False):
        """
        Transition en plein écran
        Bruits de pas enclenché
        Lancement transition
        """
        self.grid(row=0, column=0, sticky="NSWE")
        # bruits de pas
        if walk:
            print("marche...")
            # pygame.mixer.music.load("son/actions jeu/bruits-pas-son.mp3")
            # pygame.mixer.music.play(loops=0)
            walk_sound_path = "son/actions jeu/bruits-pas-son.mp3"
            walk_sound = pygame.mixer.Sound(walk_sound_path)
            walk_sound_channel.play(walk_sound)
            self.is_walk_transition = True
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
                if self.is_walk_transition:
                    walk_sound_channel.stop()
                    # pygame.mixer.music.stop()
                    # pygame.mixer.music.unload()
                self.master.check_game_events()
                self.fade_transition_ended = False


class FadeIn:
    """
    Transition de type fondu
        - fin dessin --> fade-in
        """
    def __init__(self, master):
        self.master = master
        self.imgs = ["./images/connect the dots/ref/Fish.png",
                     "./images/connect the dots/ref/ChatIRL.png",
                     "./images/connect the dots/ref/WolfSide.png",
                     "./images/connect the dots/ref/Werewolf.png",
                     "./images/connect the dots/ref/RorschackInktAlien.png"
                     ]
        # self.imgs = ["./images/connect the dots/ref/RorschackInktAlien.png"]
        self.initial_img = None
        self.pic_list = []
        self.fadetime = 1  # temps nécessaire entre temp img (effet fade) en ms
        self.fadestep = 2  # brutalité changement de transparence
        self.curstep = 0  # étape du fade in

    def initialiasize_pic(self):
        print(self.master.game_e_handler.index_dot)
        im_file = open(self.imgs[self.master.game_e_handler.index_dot], mode="rb")
        current_im = Image.open(im_file)
        alpha = min(self.curstep * self.fadestep, 255)  # clamp to 255 maximum
        current_im.putalpha(alpha)
        pic = ImageTk.PhotoImage(current_im)
        self.pic_list.append(pic)
        return pic, alpha

    def fade_in(self):
        """
        Transition en plein écran
        Bruits de pas enclenché
        Lancement transition
        """
        pic, alpha = self.initialiasize_pic()
        self.initial_img = self.master.rect.canvas.create_image(screen_width / 2, screen_height / 2, image=pic)
        self.pic_list.append(self.initial_img)
        # self.place(x=100, y=100)
        self.update_label()

    def update_label(self):
        """
        Changement blanc --> noir progressif (t)
        Quand transition stop --> fin bruits de pas
        """
        pic, alpha = self.initialiasize_pic()
        self.master.rect.canvas.itemconfigure(self.initial_img, image=pic)
        self.curstep += 2
        print('fade in: %i' % alpha)
        if alpha == 255:
            self.curstep = 0
            self.master.after(1500, self.master.dots.next_drawing)
        else:
            self.master.after(self.fadetime, self.update_label)


