import tkinter as tk
from images import bg_image_setup, set_bg


class App(tk.Tk):
    """
    Application:
        [...]
    """
    def __init__(self):
        super().__init__()
        self.title("Mon nom est...")
        self.index = 2
        self.pages_name = ["room_2", "room_1", "room_0", "room1", "room2"]
        self.pages = {
            "room_2": bg_image_setup("./images/rooms/bathrooom.png"),
            "room_1": bg_image_setup("./images/rooms/bedroom_kobe.png"),
            "room_0": bg_image_setup("./images/rooms/bedroom_test.png"),
            "room1": bg_image_setup("./images/rooms/draw_room.png"),
            "room2": bg_image_setup("./images/rooms/library_room.png")
        }
        self.initial_bg(self.pages_name[self.index])
        # dimensions écran
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.width = int(self.screen_width / 2)
        self.height = int(self.screen_height / 2)
        # position x et y centre écran
        self.center_x = int((self.screen_width / 4))
        self.center_y = int((self.screen_height / 4))
        # application dimensions initiales à fenêtre + centre fenêtre
        self.geometry("{0}x{1}+{2}+{3}".format(
            self.width, self.height, self.center_x, self.center_y
        )
        )
        # widgets
        self.view = View(self)
        self.fw = FullScreenWindow(self)
        self.c = Control(self)
        # self.r = RoomModel(self)

    def initial_bg(self, bg_name):
        set_bg(self, self.pages.get(bg_name))


class View(tk.Frame):
    """
    Fenêtre principale
    """
    def __init__(self, master):
        super().__init__(master)

    def change_room(self, room_name):
        set_bg(self.master, self.master.pages.get(room_name))


class Control(tk.Frame):
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
            self.master.index -= 1
            self.master.view.change_room(self.master.pages_name[self.master.index])
        else:
            print("C'est un mur...")
        return "break"

    def change_room_right(self, event=None):
        if self.master.index < 4:
            self.master.index += 1
            self.master.view.change_room(self.master.pages_name[self.master.index])
        else:
            print("C'est un mur...")
        return "break"


class FullScreenWindow(tk.Frame):
    """
    Événements gérés:
    - plein écran <F11> ou <Fn> + <F11>
    - <Escape> pour quitter plein écran
    """

    def __init__(self, master):
        super().__init__(master)
        self.is_fullscreen = False
        self.is_same_action = 0
        # self.pages
        master.bind("<F11>" or "<Fn> + <F11>", self.toggle_fullscreen)
        master.bind("<Escape>", self.exit_fullscreen)

    def toggle_fullscreen(self, event=None):
        if self.is_same_action == 0:
            self.is_fullscreen = not self.is_fullscreen  # toggle boolean
            self.master.attributes("-fullscreen", self.is_fullscreen)
            self.is_same_action += 1  # plein écran ne peut  qu'augmenter de 1 self.is_same action
        else:
            pass
        return "break"

    def exit_fullscreen(self, event=None):
        if self.is_same_action == 1:
            self.is_fullscreen = not self.is_fullscreen  # toggle boolean self.is_fullscreen
            self.master.attributes("-fullscreen", self.is_fullscreen)
            self.is_same_action -= 1  # réduire écran ne peut faire que diminuer de 1 self.is_same action
        return "break"


if __name__ == "__main__":
    # w = FullScreenWindow(root)
    App().mainloop()
