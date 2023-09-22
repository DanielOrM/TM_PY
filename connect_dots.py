"""Utilisation de openCV python (cv2) pour détecter
position points (x,y) et ensuite les dessiner sur CanvasHandler"""
from threading import Timer
from tkinter import Label
import cv2 as cv
import pygame
import re
from global_var import screen_width, screen_height


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

    def get_connect_dots_position(self, image_file):
        """
        Obtient position points
        Return liste des tous les points (x,y) (centre)
        """
        # Load image, filtre gris et tresh
        image = cv.imread(image_file)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

        # filtre kernel
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
        opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=3)

        # Find circles et position x,y
        cnts = cv.findContours(opening, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        list_dots_position = []
        for c in cnts:
            # cv.contourArea(c)
            M = cv.moments(c)
            # print(M)
            x_center = int(M['m10'] / M['m00'])
            y_center = int(M['m01'] / M['m00'])
            list_dots_position.append((x_center, y_center))
            # print(f"{i} et x:{x_center}, y:{y_center}")
        self.dots_list = list_dots_position
        return list_dots_position

    def helper(self, img):
        return lambda event: self.is_dot_hovered(img)

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
            # print(self.master.rect.canvas.itemconfig(img))
            # print(self.master.rect.canvas.itemconfig(img))
            self.current_dots_img.append(img)
            # self.master.rect.canvas.tag_bind(img, "<Enter-B1>", self.helper(img))
            # self.master.bind("<B1-Motion>", lambda x: print("hehehehe"))

    def is_dot_hovered(self, dot):
        # print(dot)
        # match x et y pos label
        # print(len(self.current_dots_img))
        num_dot_string = self.master.rect.canvas.itemcget(dot, "tag")
        num_dot = int(re.search(r'\d+', num_dot_string).group())
        if self.prev_dot_num == num_dot:
            print("Lent!")
            print(num_dot)
            print(self.current_dot)
            return
        elif self.current_dot != num_dot:
            if self.current_dots_img:
                for img in self.current_line_img:
                    self.master.rect.canvas.delete(img)
            self.current_dot = 0
            print("OUPS! Mauvais point!!!!!")
            print(num_dot)
            print(self.current_dot)
        else:
            print(f"C'est le point {num_dot}")
            self.prev_dot_num = self.current_dot
            self.current_dot += 1
            if self.current_dot == len(self.current_dots_img):
                print("Fini dessin!")
                self.master.fade_in.fade_in()
            print(f"Le prochain point est {self.current_dot}")
        # print(type(num_dot))

    def next_drawing(self):
        self.master.fade_in.place_forget()
        if self.master.game_e_handler.index_dot < len(self.master.game_e_handler.img_list) - 1:
            self.master.game_e_handler.index_dot += 1
        else:
            print("ATTENDRE NOUVELLE UPDATE")
            self.reset()
            return
        self.reset()
        self.master.game_e_handler.are_dots_drawn = False

    def index(self, labels_list, f):
        return next((i for i in range(len(labels_list)) if f(labels_list[i])), None)

    def find_label(self, labels_list, num_label):
        return labels_list[self.index(labels_list, lambda item: item["text"] == num_label)]

    def place_label(self, dots_list):
        for i, dots in enumerate(dots_list):
            label = Label(self.master.rect.canvas, text=f"{i}")
            label.place(x=dots[0] + CENTER_POSITION_X + 10, y=dots[1] + CENTER_POSITION_Y - 15)
            self.current_labels.append(label)

    def get_x_y(self, mouse_position):
        """
        x,y quand "paint" activé
        """
        self.lastx, self.lasty = mouse_position.get("x"), mouse_position.get("y")
        # self.highlightNext()

    def run_scheduled_task(self):
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
            print("JUSTE UNE FOIS")
            pygame.mixer.music.play(-1)
            self.has_music_started = True
        else:
            pygame.mixer.music.unpause()
        x = mouse_position.get("x")
        y = mouse_position.get("y")
        img = self.master.rect.canvas. \
            create_line((self.lastx, self.lasty, x, y), fill="black", width=1)
        self.current_line_img.append(img)
        self.lastx, self.lasty = mouse_position.get("x"), mouse_position.get("y")
        closest_canvas_items = self.master.rect.canvas.find_overlapping(self.lastx, self.lasty, x, y)
        if len(closest_canvas_items) == 3 and not self.dot_hovering:
            dot_id = closest_canvas_items[1]
            self.is_dot_hovered(dot_id)
            self.run_scheduled_task()
            self.dot_hovering = True
            # self.is_dot_hovered(dot_id)

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
        # print(self.current_dots_img)
        # print(self.current_line_img)
        # print(self.current_labels)
        self.current_dots_img, self.current_line_img, self.dots_list, self.current_labels = [], [], [], []

    def start_game(self, image_file):
        # self.get_connect_dots_position(image_file)
        self.sort_points(image_file)
        self.place_dots(self.dots_list)
        self.place_label(self.dots_list)

    def sort_points(self, img):
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
        # print(len(self.dots_list))
        # print("duh1")
        # print("duh2")
        # print(self.dots_list[len(self.dots_list)-1])
        # print(self.dots_list[40])
        return self.dots_list
