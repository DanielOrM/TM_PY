"""Utilisation de openCV python (cv2) pour détecter
position points (x,y) et ensuite les dessiner sur CanvasHandler"""
import threading
from threading import Timer
from tkinter import Label
import re
import cv2 as cv
import pygame
from PIL import Image, ImageTk
from global_var import screen_width, screen_height
from images import bg_image_setup
from son.random_sound_effects import SetInterval
from son.channels import pen_channel

CENTER_POSITION_X = screen_width / 5
CENTER_POSITION_Y = screen_height / 4


class ConnectDotsGame:
    """
    Jeu "connect the dots" dans pyimage8
    --> manque encore connexion entre points (jeu)
    Résolution img:
        - 560
        - 330
    """

    def __init__(self, master):
        self.master = master
        self.current_dots_img = []
        self.current_line_img = []
        self.current_labels = []
        self.lastx = None
        self.lasty = None
        # pygame
        self.has_music_started = False
        # setup pour début jeu
        self.dots_list = []
        self.current_dot = 0
        self.dot_hovering = False
        self.prev_dot_num = None

        # monstre
        self.monster_img = None
        self.monster_final_img = None
        self.monster_img_list = []
        self.monster_canvas_item = None
        self.monster_smile_timer = None
        self.t_w = None
        self.t_b = None
        self.w_b_delay = 0.2

        # écran noir
        self.black_background = bg_image_setup("./images/monster/BlackBackground.png", name="screamer écran noir")
        self.white_background = bg_image_setup("./images/monster/WhiteBackground.png", name="screamer écran blanc")

    def place_dots(self, dots_position):
        """
        Position des points connues
        Chaque point --> placé dans self.current_dots_img
        """
        for i, d in enumerate(dots_position):
            x1, y1 = (d[0] + CENTER_POSITION_X - 3), (d[1] + CENTER_POSITION_Y - 3)
            x2, y2 = (d[0] + CENTER_POSITION_X + 3), (d[1] + CENTER_POSITION_Y + 3)
            canvas = self.master.rect.canvas
            img = canvas.create_oval(x1, y1, x2, y2, fill="black", tag=i)
            self.current_dots_img.append(img)

    def is_dot_hovered(self, dot):
        """
        Check quel point a été hover pendant dessin
        - obtient numéro (text) à partir de tag dot
        """
        num_dot_string = self.master.rect.canvas.itemcget(dot, "tag")
        num_dot = int(re.search(r'\d+', num_dot_string).group())
        if self.prev_dot_num == num_dot:
            return
        if self.current_dot != num_dot:
            if self.current_dots_img:
                for img in self.current_line_img:
                    self.master.rect.canvas.delete(img)
            self.current_dot = 0
        else:
            # print(f"C'est le point {num_dot}")
            self.prev_dot_num = self.current_dot
            self.current_dot += 1
            if self.current_dot == len(self.current_dots_img):
                self.master.fade_in.fade_in()
            # print(f"Le prochain point est {self.current_dot}")

    def next_drawing(self):
        """
        Passe au prochain dessin dans liste (self.master.game_e_handler.img_list)
        """
        ref_pic = self.master.fade_in.initial_img
        self.master.rect.canvas.delete(ref_pic)
        if self.master.game_e_handler.index_dot < len(self.master.game_e_handler.img_list) - 1:
            self.master.game_e_handler.index_dot += 1
        else:
            self.master.game_e_handler.has_monster_appeared = True
            self.reset()
            # monstre appari°
            t = threading.Timer(1, self.activate_monster_smile)
            t.start()
            self.master.rect.canvas.bind("<Button-1>", lambda event: self.screamer)
            return
        self.reset()
        self.master.game_e_handler.are_dots_drawn = False

    def index(self, labels_list, f):
        """
        Return index pour chaque clef d'un label
        """
        return next((i for i in range(len(labels_list)) if f(labels_list[i])), None)

    def find_label(self, labels_list, num_label):
        """
        Trouve label basé sur une clef ET valeur particulière
        """
        return labels_list[self.index(labels_list, lambda item: item["text"] == num_label)]

    def place_label(self, dots_list):
        """
        Place label sur canvas (légèrement en haut à droite de position dot)
        """
        for i, dots in enumerate(dots_list):
            label = Label(self.master.rect.canvas, text=f"{i}", font=("Calibri", 9))
            label.place(x=dots[0] + CENTER_POSITION_X + 5, y=dots[1] + CENTER_POSITION_Y - 10)
            self.current_labels.append(label)

    def get_x_y(self, mouse_position):
        """
        x,y quand "paint" activé
        """
        self.lastx, self.lasty = mouse_position.get("x"), mouse_position.get("y")

    def check_point_delay(self):
        """
        Évite de recommencer à chaque fois (call func pour point plus d'une fois)
        """
        timer = Timer(0.25, self.toggle_dot_hovering)
        timer.start()

    def toggle_dot_hovering(self):
        """
        Possibilité de trouver prochain point (réactivé)
        """
        self.dot_hovering = False

    def paint(self, mouse_position):
        """
        Trace ligne continue et lance musique
        Musique arrête si func paint =/ appelée
        """
        if not self.has_music_started:
            # une fois
            pen_sound_path = "son/actions jeu/son-écrit-crayon.mp3"
            pen_sound = pygame.mixer.Sound(pen_sound_path)
            pen_channel.play(pen_sound, loops=-1)
            self.has_music_started = True
        else:
            pen_channel.unpause()
        x = mouse_position.get("x")
        y = mouse_position.get("y")
        img = self.master.rect.canvas. \
            create_line((self.lastx, self.lasty, x, y), fill="black", width=1)
        self.current_line_img.append(img)
        self.lastx, self.lasty = mouse_position.get("x"), mouse_position.get("y")
        closest_canvas_items = self.master.rect.canvas. \
            find_overlapping(self.lastx, self.lasty, x, y)
        if len(closest_canvas_items) == 3 and not self.dot_hovering:
            dot_id = closest_canvas_items[1]
            self.is_dot_hovered(dot_id)
            self.check_point_delay()
            self.dot_hovering = True

    def reset(self):
        """
        Enlève les points + ligne quand change de pièce
        """
        # condition évite erreur avec liste(=vide)
        self.current_dot = 0
        if self.current_dots_img:
            for img in self.current_dots_img:
                self.master.rect.canvas.delete(img)
            for img in self.current_line_img:
                self.master.rect.canvas.delete(img)
            for label in self.current_labels:
                label.place_forget()
        self.current_dots_img, self.current_line_img, \
        self.dots_list, self.current_labels = [], [], [], []

    def start_game(self, image_file):
        """
        Lance jeu pour 1 dessin
        """
        self.sort_points(image_file)
        self.place_dots(self.dots_list)
        self.place_label(self.dots_list)

    def sort_points(self, img):
        """
        Obtient position de tous les points
            - points triés par ordre de grandeur
            - self.dots_list = liste points ordonnés
        Plusieurs filtres pour 1 image sont appliqués
        """
        image = cv.imread(img)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        edged = cv.Canny(gray, 50, 200)
        contours, hierarchy = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        all_areas = []
        for d in contours:
            area = cv.contourArea(d)
            all_areas.append(area)
        sorted_contours = sorted(contours, key=cv.contourArea)
        for i in sorted_contours:
            M = cv.moments(i)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                dot_position = (cx, cy)
                self.dots_list.append(dot_position)
        return self.dots_list

    def screamer(self):
        """
        Appari° monstre, zoom avec délai
        """
        self.all_black_and_monster()
        self.epileptic_background(self.w_b_delay)  # changement noir/blanc chaque 0.1s
        remove_epileptic_bg_timer = threading.Timer(3, self.remove_epileptic_bg)  # pendant 3s
        remove_epileptic_bg_timer.start()

    def all_white(self):
        self.master.rect.change_background("app_background", self.white_background)
        self.master.rect.changing_state_canvas_item(self.monster_canvas_item, "normal")

    def all_black_and_monster(self):
        self.master.rect.change_background("app_background", self.black_background)
        self.master.rect.changing_state_canvas_item(self.monster_canvas_item, "hidden")

    def epileptic_background(self, sec):
        white_timer = threading.Timer(sec, self.white_inter)
        white_timer.start()
        black_and_monster_timer = threading.Timer(sec*2, self.black_monster_inter)
        black_and_monster_timer.start()

    def white_inter(self):
        self.all_white()
        self.t_w = SetInterval(self.all_white, self.w_b_delay*2)

    def black_monster_inter(self):
        self.all_black_and_monster()
        self.t_b = SetInterval(self.all_black_and_monster, self.w_b_delay*2)

    def remove_epileptic_bg(self):
        self.t_w.cancel()
        self.t_b.cancel()
        self.master.rect.changing_state_canvas_item(self.monster_canvas_item, "hidden")
        self.master.rect.change_background("app_background", "pièce dessin")
        self.master.game_e_handler.has_monster_appeared = True

    def activate_monster_smile(self):
        """
        Scène monstre activée par cette func
        Instance toutes les images nécessaires
            - self.monster_img
            - self.monster_final_img
            - panel
            - self.monster_canvas_item
        """
        print("START MONSTER")
        self.monster_img = Image.open("./images/monster/PA_NB_SourireMonstre.png")
        self.monster_final_img = ImageTk.PhotoImage(image=self.monster_img)
        self.monster_img_list.append(self.monster_final_img)
        panel = self.master.rect.canvas.create_image(screen_width / 2, screen_height / 2, image=self.monster_final_img)
        print(panel)
        self.monster_canvas_item = panel
        self.monster_img_list.append(panel)
        self.monster_smile_timer = SetInterval(self.monster_resize, 0.2)

    def monster_resize(self):
        """
        Change la taille de l'image sourire monstre chaque 0.2s
        Écran noir quand sourire atteint la hauteur de l'écran
        """
        print("scaling monster img")
        pic_width, pic_height = self.monster_final_img.width(), self.monster_final_img.height()
        pic_width_tenth, pic_height_tenth = int(pic_width / 10), int(pic_height / 10)
        if pic_height >= screen_height:
            print("")
            self.monster_smile_timer.cancel()
            self.screamer()
        new_image_resized = self.monster_img.resize \
            ((pic_width + pic_width_tenth, pic_height + pic_height_tenth))
        self.monster_final_img = ImageTk.PhotoImage(image=new_image_resized)
        self.master.rect.canvas.itemconfigure(self.monster_canvas_item, image=self.monster_final_img)
