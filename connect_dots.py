"""Utilisation de openCV python pour détecter positions points (x,y) et ensuite les dessiner sur CanvasHandler"""
import cv2 as cv
from global_var import screen_width, screen_height

CENTER_POSITION_X = screen_width / 5
CENTER_POSITION_Y = screen_height / 4


class ConnectDotsGame:
    def __init__(self, master):
        self.master = master
        self.current_dots_img = []
        self.current_drawing = []
        self.lastx = None
        self.lasty = None

    def get_connect_dots_position(self, image_file):
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
        for i, c in enumerate(cnts):
            area = cv.contourArea(c)
            M = cv.moments(c)
            x_center = int(M['m10'] / M['m00'])
            y_center = int(M['m01'] / M['m00'])
            list_dots_position.append((x_center, y_center))
            # print(f"{i} et x:{x_center}, y:{y_center}")
            if 20 < area < 50:
                ((x, y), r) = cv.minEnclosingCircle(c)
                print(x, y)
                cv.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)

        return list_dots_position

    def place_dots(self, dots_position):
        for d in dots_position:
            x1, y1 = (d[0] + CENTER_POSITION_X - 3), (d[1] + CENTER_POSITION_Y - 3)
            x2, y2 = (d[0] + CENTER_POSITION_X + 3), (d[1] + CENTER_POSITION_Y + 3)
            img = self.master.rect.canvas.create_oval(x1, y1, x2, y2, fill="black")
            self.current_dots_img.append(img)

    def get_x_y(self, mouse_position):
        self.lastx, self.lasty = mouse_position.get("x"), mouse_position.get("y")

    def paint(self, mouse_position):
        x = mouse_position.get("x")
        y = mouse_position.get("y")
        img = self.master.rect.canvas.create_line((self.lastx, self.lasty, x, y), fill="black", width=1)
        self.current_drawing.append(img)
        self.lastx, self.lasty = mouse_position.get("x"), mouse_position.get("y")

    def reset(self):
        # condition évite erreur avec liste(=vide)
        if self.current_dots_img and self.current_drawing:
            for img in self.current_dots_img:
                self.master.rect.canvas.delete(img)
            for img in self.current_drawing:
                self.master.rect.canvas.delete(img)
        self.current_dots_img, self.current_drawing = [], []

