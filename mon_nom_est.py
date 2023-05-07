import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    """
    Application:
        Attributs:
        - fenêtre principale
    """

    def __init__(self):
        super().__init__()
        self.title("Mon nom est...")
        # dimensions écran
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.width = int(self.screen_width/2)
        self.height = int(self.screen_height/2)
        # position x et y du centre écran
        self.center_x = int((self.screen_width/4))
        self.center_y = int((self.screen_height/4))
        # applique dimensions initiales à fenêtre + centre fenêtre
        self.geometry("{0}x{1}+{2}+{3}".format(
            self.width, self.height, self.center_x, self.center_y
            )
        )
        # widgets
        self.w = FullScreenWindow(self)


class FullScreenWindow(ttk.Frame):
    """
    Événements gérés:
    - plein écran <F11>
    - <Escape> pour quitter plein écran
    """
    def __init__(self, master):
        super().__init__(master)
        self.is_fullscreen = False
        self.is_same_action = 0
        master.bind("<F11>" or "<Fn> + <F11>", self.toggle_fullscreen)
        master.bind("<Escape>", self.exit_fullscreen)

    def toggle_fullscreen(self, event):
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


if __name__ == "__main__":
    # w = FullScreenWindow(root)
    App().mainloop()
