"""Transition de type fondu"""
import tkinter as tk
import pygame
from PIL import ImageTk, Image
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
        self.start_color = label_background_8_bit_color  # blanc
        self.end_color = tuple((0, 0, 0))  # noir
        # lapse de temps
        self.duration_ms = 1000
        self.frames_per_second = 60
        self.ms_sleep_duration = 1000 // self.frames_per_second
        self.current_step = 0
        self.fade_transition_ended = False
        self.is_walk_transition = False

    def create_transition(self, walk=False):
        """
        Transition en plein écran
        Bruits de pas enclenché
        Lancement transition
        """
        self.grid(row=0, column=0, sticky="NSWE")
        # bruits de pas
        if walk:
            walk_sound_path = "son/actions jeu/bruits-pas-son.mp3"
            walk_sound = pygame.mixer.Sound(walk_sound_path)
            walk_sound_channel.play(walk_sound)
            walk_sound_channel.set_volume(0.4)
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
                self.master.check_game_events()
                self.fade_transition_ended = False


class FadeIn:
    """
    Transition de type fondu
        - fin dessin --> fade-in
        """

    def __init__(self, master):
        self.master = master
        # self.base_file_img_ref = "./images/connect the dots/ref/"
        self.imgs = ["./images/connect the dots/ref/Fish.png",
                     "./images/connect the dots/ref/ChatIRL.png",
                     "./images/connect the dots/ref/WolfSide.png",
                     "./images/connect the dots/ref/Werewolf.png",
                     "./images/connect the dots/ref/RorschackInktAlien.png"
                     ]
        # self.imgs = ["./images/connect the dots/ref/Fish.png"]
        self.initial_img = None
        self.middle_x_point = None
        self.middle_y_point = None
        self.pic_list = []
        # item dans inventaire
        self.item_text_animation = "./images/inventory/PA_NB_ItemAdded.png"
        self.fade_o_curstep = 255
        self.fadetime = 1  # temps nécessaire entre temp img (effet fade) en ms
        self.fadestep = 2  # brutalité changement de transparence
        self.fadestep_draw = 3
        self.curstep = 0  # étape du fade in

    def remove_fully_transparent_pixels(self, drawing_ref, alpha, base_folder="./images/connect the dots/fade img/",
                                        base_file_img_ref="./images/connect the dots/ref/", event=None):
        """
        Enlève bg transparent d'img
        """
        # channel alpha
        img = Image.open(drawing_ref)
        A = img.getchannel("A")
        # blanc en opaque
        newA = A.point(lambda i: alpha if i > 0 else 0)
        # pixels modifiés + overwrite dans nouvelle image
        img.putalpha(newA)
        img_ref_name = drawing_ref.replace(base_file_img_ref, "")
        final_path = base_folder + img_ref_name
        img.save(final_path)
        return final_path

    def initialiasize_pic(self):
        """
        Crée diff. versions de la même img en plusieurs opacités
        """
        drawing_ref = self.imgs[self.master.game_e_handler.index_dot]
        alpha = min(self.curstep * self.fadestep_draw, 255)  # clamp to 255 maximum
        modified_img = self.remove_fully_transparent_pixels(drawing_ref, alpha)
        current_im = Image.open(modified_img)
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
        # print(self.middle_x_point, self.middle_y_point)
        self.initial_img = self.master.rect.canvas.create_image(self.middle_x_point, self.middle_y_point, image=pic)
        self.pic_list.append(self.initial_img)
        self.update_label()

    def update_label(self):
        """
        Changement blanc --> noir progressif (t)
        Quand transition stop --> fin bruits de pas
        """
        pic, alpha = self.initialiasize_pic()
        self.master.rect.canvas.itemconfigure(self.initial_img, image=pic)
        self.curstep += 2
        if alpha == 255:
            self.curstep = 0
            self.master.after(1500, self.master.dots.next_drawing)
        else:
            self.master.after(self.fadetime, self.update_label)

    def initialiasize_text(self, fade_out=False):
        """
        Début avec texte (=/opaque ou opaque)
        """
        pic_size = (120, 30)
        if not fade_out:
            alpha = min(self.curstep * self.fadestep, 255)  # clamp to 255 maximum
            modified_img = self.remove_fully_transparent_pixels(self.item_text_animation, alpha,
                                                                "./images/inventory/text animation/",
                                                                "./images/inventory/")
            current_im = Image.open(modified_img)
            pic = ImageTk.PhotoImage(current_im.resize(pic_size))
            self.pic_list.append(pic)
            return pic, alpha
        else:
            alpha = max(self.fade_o_curstep * self.fadestep, 0)  # clamp to 0 maximum
            modified_img = self.remove_fully_transparent_pixels(self.item_text_animation, alpha,
                                                                "./images/inventory/text animation/",
                                                                "./images/inventory/"
                                                                )
            current_im = Image.open(modified_img)
            pic = ImageTk.PhotoImage(current_im.resize(pic_size))
            self.pic_list.append(pic)
            return pic, alpha

    def update_text(self, fade_out=False):
        """
        Changement blanc --> noir progressif (t)
        Quand transition stop --> fin bruits de pas
        """
        if not fade_out:
            pic, alpha = self.initialiasize_text()
            self.master.rect.canvas.itemconfigure(self.initial_img, image=pic)
            self.curstep += 2
            if alpha == 255:
                self.curstep = 0
                self.master.after(200, self.fade_out)
            else:
                self.master.after(self.fadetime, self.update_text)
        else:
            pic, alpha = self.initialiasize_text(True)
            self.master.rect.canvas.itemconfigure(self.initial_img, image=pic)
            self.fade_o_curstep -= 2
            if alpha == 0:
                print("NOPE NOPE NOPE")
                self.fade_o_curstep = 255
            else:
                self.master.after(self.fadetime, self.update_text, True)

    def start_item_animation(self):
        """
        Lance animation quand ajoute obj à inventaire
        """
        pic, alpha = self.initialiasize_text()
        # print(self.middle_x_point, self.middle_y_point)
        self.initial_img = self.master.rect.canvas.create_image(
            (self.master.screen_width/6*5, self.master.screen_height*0.8),
            image=pic)
        self.pic_list.append(self.initial_img)
        self.update_text()

    def fade_out(self):
        """
        255 --> 0 (opaque --> =/opaque)
        """
        pic, alpha = self.initialiasize_text(True)
        self.master.rect.canvas.itemconfigure(self.initial_img, image=pic)
        self.update_text(True)
