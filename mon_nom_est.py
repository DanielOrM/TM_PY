import tkinter as tk
from tkinter import ttk


# class RoomModel(ttk.Frame):
#     def __init__(self, png):  # couleur pour tester puis ce sera changé en png pour chaque pièce
#         super().__init__(png)
#         self.png = png
#         self.configure(background="{0}".format(png))
#
#
# Room1 = RoomModel("blue")
# Room2 = RoomModel("green")


class App(tk.Tk):
    """
    Application:
        Attributs:
        - fenêtre principale
    """

    def __init__(self):
        super().__init__()
        self.title("Mon nom est...")
        self.index = 2
        self.bg = None
        # toutes les pièces (couleurs) dans une liste, pièce initiale = 0
        # chaque couleur = 1 pièce, TEMPORAIRE (après png)
        # self.COLORS = [(""), #
        #                (), # -2 -1, -2=DERNIÈRE PIÈCE
        #                (), # -2 -1 0
        #                (), # -1, 0, 1
        #                (), # 0 1 2
        #                (), # 1 2, 2=DERNIÈRE PIÈCE
        #     ]
        self.COLORS = ["red", "blue", "green", "yellow", "pink"]
        # self.ROOMS = [Room1, Room2, "blue"]
        self.configure(background="{0}".format(self.COLORS[self.index]))
        # self.configure(background="{0}".format(self.ROOMS[self.index]))
        # self.configure()
        # dimensions écran
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.width = int(self.screen_width/2)
        self.height = int(self.screen_height/2)
        # position x et y centre écran
        self.center_x = int((self.screen_width/4))
        self.center_y = int((self.screen_height/4))
        # application dimensions initiales à fenêtre + centre fenêtre
        self.geometry("{0}x{1}+{2}+{3}".format(
            self.width, self.height, self.center_x, self.center_y
            )
        )
        # widgets
        self.w = FullScreenWindow(self)
        self.c = Control(self)
        # self.r = RoomModel(self)


class FullScreenWindow(ttk.Frame):
    """
    Événements gérés:
    - plein écran <F11> ou <Fn> + <F11>
    - <Escape> pour quitter plein écran
    """
    def __init__(self, master):
        super().__init__(master)
        self.is_fullscreen = False
        self.is_same_action = 0
        master.bind("<F11>" or "<Fn> + <F11>", self.toggle_fullscreen)
        master.bind("<Escape>", self.exit_fullscreen)

    def toggle_fullscreen(self, event=None):
        if self.is_same_action == 0:
            self.is_fullscreen = not self.is_fullscreen  # toggle boolean
            self.master.attributes("-fullscreen", self.is_fullscreen)
            self.is_same_action += 1    # plein écran ne peut  qu'augmenter de 1 self.is_same action
        else:
            pass
        return "break"

    def exit_fullscreen(self, event=None):
        if self.is_same_action == 1:
            self.is_fullscreen = not self.is_fullscreen  # toggle boolean self.is_fullscreen
            self.master.attributes("-fullscreen", self.is_fullscreen)
            self.is_same_action -= 1    # réduire écran ne peut faire que diminuer de 1 self.is_same action
        return "break"


# class View(tk.Frame):
#     def __init__(self, master):
#         """Peupler la vue."""
#         super().__init__(master)


# class Controle:
#     """Contrôle de l'application.
#
#     Attributs:
#     - vue: la Vue de l'application.
#     - plein écran <F11> puis <Escape> pour quitter plein écran
#
#     Événements gérés:
#     - à faire...
#     """
#
#     def __init__(self):
#         pass


class Control(ttk.Frame):
    """
    Événements gérés:
    -
    """
    def __init__(self, master):
        super().__init__(master)
        master.bind("<a>", self.change_room_left)
        master.bind("<d>", self.change_room_right)

    def change_room_left(self, event=None):
        if self.master.index > 0:
            # room_chosen = self.master.COLORS[index_room]
            self.master.index -= 1
            index_room = self.master.index
            self.master.configure(background="{0}".format(self.master.COLORS[index_room]))
            # self.master.configure(background="{0}".format(self.master.ROOMS[index_room]))
            print("TEST")
        else:
            print("C'est un mur...")
        return "break"

    def change_room_right(self, event=None):
        if self.master.index < 4:
            # room_chosen = self.master.COLORS[index_room]
            self.master.index += 1
            index_room = self.master.index
            self.master.configure(background="{0}".format(self.master.COLORS[index_room]))
            # self.master.configure(background="{0}".format(self.master.ROOMS[index_room]))
            print("TEST")
        else:
            print("C'est un mur...")
        return "break"


if __name__ == "__main__":
    # w = FullScreenWindow(root)
    App().mainloop()
