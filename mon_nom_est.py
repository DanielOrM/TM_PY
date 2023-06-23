import tkinter as tk
from tkinter import VERTICAL, HORIZONTAL

from images import bg_image_setup, open_image_setup


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
        self.camera = open_image_setup("./images/player/PA_NB_PhotoCameraFromBehind.png").subsample(2,2) # image caméra 2 fois plus petite
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
        self.rect = PictureCropRect(self) # rectangle photo dimensions
        # self.r = RoomModel(self)

    def initial_bg(self, bg_name):
        # set_bg(self, self.pages.get(bg_name))
        pass


class View(tk.Frame):
    """
    Fenêtre principale
    """
    def __init__(self, master):
        super().__init__(master)

    def change_room(self, room_name):
        # set_bg(self.master, self.master.pages.get(room_name)) # cherche nom de pièce + applique image correspondante
        PCR = PictureCropRect.__init__(PictureCropRect(self.master), self.master)
        PCR.canvas.itemconfig(
            PictureCropRect.__init__(PictureCropRect(self.master), self.master).background,
            room_name
        ) # change image du canvas
    # def pic_rec_maker_on_mouse_click(self, event):
    #     # dimensions photo création
    #     print("TEST FOR X: {0}".format(event.x))
    #     picture_rec = tk.Canvas(self.master)
    #     picture_rec.rect = None
    #     picture_rec.start_x = event.x
    #     picture_rec.start_y = event.y
    #     picture_rec.create_rectangle((picture_rec.start_x, picture_rec.start_y,1,1), fill="black")
    #     picture_rec.pack(fill="both", expand=True)
        # picture_rec.create_rectangle((100,100, 50, 50), outline="yellow")


class Control(tk.Frame):
    """
    Événements gérés:
    -
    """

    def __init__(self, master):
        super().__init__(master)
        master.bind("<a>", self.change_room_left) # aller à gauche
        master.bind("<d>", self.change_room_right) # aller à droite
        master.bind("<Button-3>", self.take_picture) # button 3 => click droit

    def change_room_left(self, event=None):
        if self.master.index > 0:
            self.master.index -= 1
            print(self.master.index)
            self.master.view.change_room(self.master.pages_name[self.master.index]) # argument = nom de la pièce
        else:
            print("C'est un mur...")
        return "break"

    def change_room_right(self, event=None):
        if self.master.index < 4:
            self.master.index += 1
            print(self.master.index)
            self.master.view.change_room(self.master.pages_name[self.master.index])
        else:
            print("C'est un mur...")
        return "break"

    def take_picture(self, event):
        # x = self.master.winfo_pointerx()
        # print(x)
        print("Hey! I'm a single click")
        # self.master.view.pic_rec_maker_on_mouse_click(event)


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


class PictureCropRect(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.x = self.y = 0
        self.canvas = tk.Canvas(self.master, cursor="cross",
                                height=self.master.winfo_screenheight(), width=self.master.winfo_screenwidth(),
                                )
        self.background = self.canvas.create_image(self.master.winfo_screenwidth()/2, self.master.winfo_screenheight()/2,
                                                   image=self.master.pages.get(self.master.pages_name[self.master.index])
                                                   )
        self.camera = self.canvas.create_image(self.master.winfo_screenwidth()/2, self.master.winfo_screenheight()/1.5,
                                               image=self.master.camera
                                               )
        self.sbarv = tk.Scrollbar(self, orient=VERTICAL)
        self.sbarh = tk.Scrollbar(self, orient=HORIZONTAL)
        self.sbarv.config(command=self.canvas.yview)
        self.sbarh.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=self.sbarv.set)
        self.canvas.config(xscrollcommand=self.sbarh.set)

        self.canvas.grid(row=0,column=0,sticky="NSEW")
        self.sbarv.grid(row=0,column=1,stick="NS")
        self.sbarh.grid(row=1,column=0,sticky="EW")

        self.canvas.bind("<Button-3>", self.on_button_press)
        self.canvas.bind("<B3-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-3>", self.on_button_released)

        self.rect = None
        self.start_x = None
        self.start_y = None

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='yellow', dash=(1,2))

    def on_move_press(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)
        # agrandi rectangle pendant sélection
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_released(self, event=None):
        print("FINALLY")
        self.canvas.delete(self.rect)
        self.rect = None


if __name__ == "__main__":
    # w = FullScreenWindow(root)
    App().mainloop()
