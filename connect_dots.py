"""Utilisation de openCV python (cv2) pour détecter
position points (x,y) et ensuite les dessiner sur CanvasHandler"""
import cv2 as cv
import pygame
from global_var import screen_width, screen_height

CENTER_POSITION_X = screen_width / 5
CENTER_POSITION_Y = screen_height / 4


class ConnectDotsGame:
    """
    Jeu "connect the dots" dans pyimage8
    --> manque encore connexion entre points (jeu)
    """
    def __init__(self, master):
        self.master = master
        self.current_dots_img = []
        self.current_drawing = []
        self.lastx = None
        self.lasty = None
        # pygame
        self.has_music_started = False

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
        return list_dots_position

    def place_dots(self, dots_position):
        """
        Position des points connues
        Chaque point --> placé dans self.current_dots_img
        """
        for d in dots_position:
            x1, y1 = (d[0] + CENTER_POSITION_X - 3), (d[1] + CENTER_POSITION_Y - 3)
            x2, y2 = (d[0] + CENTER_POSITION_X + 3), (d[1] + CENTER_POSITION_Y + 3)
            img = self.master.rect.canvas.create_oval(x1, y1, x2, y2, fill="black")
            self.current_dots_img.append(img)

    def get_x_y(self, mouse_position):
        """
        x,y quand "paint" activé
        """
        self.lastx, self.lasty = mouse_position.get("x"), mouse_position.get("y")

    def paint(self, mouse_position):
        """
        Trace ligne continue et lance musique
        Musique arrête si func paint =/ appelée
        """
        if not self.has_music_started:
            print("JUSTE UNE FOIS")
            pygame.mixer.music.play()
            self.has_music_started = True
        else:
            pygame.mixer.music.unpause()
        x = mouse_position.get("x")
        y = mouse_position.get("y")
        img = self.master.rect.canvas.\
            create_line((self.lastx, self.lasty, x, y), fill="black", width=1)
        self.current_drawing.append(img)
        self.lastx, self.lasty = mouse_position.get("x"), mouse_position.get("y")

    def reset(self):
        """
        Enlève les points + ligne quand change de pièce
        """
        # condition évite erreur avec liste(=vide)
        if self.current_dots_img and self.current_drawing:
            for img in self.current_dots_img:
                self.master.rect.canvas.delete(img)
            for img in self.current_drawing:
                self.master.rect.canvas.delete(img)
        self.current_dots_img, self.current_drawing = [], []
