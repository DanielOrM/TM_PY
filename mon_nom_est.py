import tkinter as tk
from tkinter import VERTICAL, HORIZONTAL

from PIL import Image, ImageTk

from images import bg_image_setup, open_image_setup_file


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
        self.pages_file_location = {
            "room_2": "./images/rooms/bathrooom.png",
            "room_1": "./images/rooms/bedroom_kobe.png",
            "room_0": "./images/rooms/bedroom_test.png",
            "room1": "./images/rooms/draw_room.png",
            "room2": "./images/rooms/library_room.png"
        }
        self.pages = {
            "room_2": bg_image_setup(self.pages_file_location.get("room_2")),
            "room_1": bg_image_setup(self.pages_file_location.get("room_1")),
            "room_0": bg_image_setup(self.pages_file_location.get("room_0")),
            "room1": bg_image_setup(self.pages_file_location.get("room1")),
            "room2": bg_image_setup(self.pages_file_location.get("room2"))
        }
        self.camera = open_image_setup_file("./images/player/PA_NB_PhotoCameraFromBehind.png").subsample(2,2) # image caméra 2 fois plus petite
        self.album = open_image_setup_file("./images/player/PA_NB_Album.png")
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
        self.rect = CanvasHandler(self) # rectangle photo dimensions
        # self.r = RoomModel(self)


class View(tk.Frame):
    """
    Fenêtre principale
    """
    def __init__(self, master):
        super().__init__(master)

    def change_room(self, room_name):
        # CH = self.master.rect
        # set_bg(self.master, self.master.pages.get(room_name)) # cherche nom de pièce + applique image correspondante
        # print("WTF")
        # CH = CanvasHandler.__init__(CanvasHandler(self.master), self.master)
        # CH.canvas.itemconfig(
        #     CanvasHandler.__init__(CanvasHandler(self.master), self.master).background,
        #     room_name
        # ) # change image du canvas
        # self.master.rect.itemconfigure(
        #     self.master.rect.background,
        #     room_name
        # )
        # self.master.rect.lower(room_name)
        # CH.configure_canvas_item(CH(self.master), app_background, room_name)
        canvas_page = self.master.rect.change_background("app_background", self.master.pages.get(f"{room_name}"))



    def show_album(self, event=None):
        self.master.rect.open_journal()
        # print("STILL THERE")


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
        master.bind("<Button-2>", self.see_album) # button 2 => mid click

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
        pass
        # print(x)
        # print("Hey! I'm a single click")
        # self.master.view.pic_rec_maker_on_mouse_click(event)

    def see_album(self, event=None):
        self.master.view.show_album()


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


class CanvasHandler(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.x = self.y = 0
        self.canvas = tk.Canvas(self.master, cursor="cross",
                                height=self.master.winfo_screenheight(), width=self.master.winfo_screenwidth(),
                                )
        self.background = self.canvas.create_image(self.master.winfo_screenwidth()/2, self.master.winfo_screenheight()/2,
                                                   image=self.master.pages.get(self.master.pages_name[self.master.index]), tag="app_background"
                                                   )
        self.camera = self.canvas.create_image(self.master.winfo_screenwidth()/2, self.master.winfo_screenheight()/1.5,
                                               image=self.master.camera
                                               )
        self.album = self.canvas.create_image(self.master.winfo_screenwidth() / 2, self.master.winfo_screenheight() / 2,
                                              image=self.master.album
                                              )
        self.canvas.itemconfigure(self.album, state="hidden")
        self.photos_list = []
        self.photos_list_updated = [] # sert à check si la liste a changé
        # print(self.canvas.itemconfigure(self.album).get("state")[4])
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
        # numéro pour id de la première image de la liste des photos
        self.initial_img_id = 0

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
        # print("FINALLY")
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)
        self.place_photo_album_list((self.start_x, self.start_y, curX, curY))
        self.canvas.delete(self.rect)
        self.rect = None

    def open_journal(self, event=None):
        # print("Hiiiiii I'm a canvas maker!")
        state = self.canvas.itemcget(self.album, "state")
        # print(state)
        if state == "hidden":
            # self.canvas.itemconfigure(self.album, state="normal")
            # self.canvas.lift(self.album, self.background)
            self.changing_state_canvas_item(self.album, "normal")
            # self.canvas.lift(self.album)
            self.show_photos_album()
            # print("I am visible!!!!!")
        elif state == "normal":
            # self.canvas.itemconfigure(self.album, state="hidden")
            self.changing_state_canvas_item(self.album, "hidden")
            # self.canvas.lower(self.album)
            self.hide_photos_album()
            # print("shhhh I am hidden...")

    def changing_state_canvas_item(self, canvas_item_id, new_state):
        self.canvas.itemconfigure(canvas_item_id, state=new_state)

    def place_photo_album_list(self, crop_dimensions):
        # ajoute photo prise dans liste des photos
        image_to_crop_temp = Image.open(self.master.pages_file_location.get(self.master.pages_name[self.master.index]))
        image_to_crop = image_to_crop_temp.resize((1920,1080)).convert("RGBA")
        # image_to_crop = self.master.pages.get(self.master.pages_name[self.master.index])
        # print(image_to_crop)
        # w, h = image_to_crop.size
        # print(image_to_crop.size)
        # print(w, h)
        # print(crop_dimensions)
        pic_taken_temp = image_to_crop.crop(crop_dimensions)
        # print(pic_taken_temp)
        # pic_taken = pic_taken_temp
        pic_taken = ImageTk.PhotoImage(pic_taken_temp)
        # pic_taken = ImageTk.PhotoImage(image_to_crop)
        self.photos_list_updated.append(pic_taken)

    def show_photos_album(self, event=None):
        # crée image pour chaque photo dans album => grid
        # print(self.photos_list)
        # print(self.photos_list_updated)
        # for image in self.photos_list_updated:
        #     print(image)
        p1 = set(self.photos_list_updated)
        p2 = set(self.photos_list)
        diff = p1.difference(p2)
        # print(diff)
        if diff:
            # print(self.photos_list_updated)
            print("SOMETHING HAS CHANGED")
            # print(self.photos_list_updated)
            # crée image juste pour image qui se trouve dans updated list
            # for id, image in enumerate(self.photos_list_updated):
            #     print(id)
            #     self.canvas.create_image(self.master.winfo_screenwidth() / 2, self.master.winfo_screenheight()/2,
            #                                     image=image, tag="pic{0}".format(id))
            #
            for id, image in enumerate(self.photos_list_updated):
                # img = str(image)
                # print(str(image))
                # print(int(''.join(list(filter(str.isdigit, img))))-4)
                # print("END")
                self.canvas.create_image(self.master.winfo_screenwidth() / 2, self.master.winfo_screenheight()/2,
                                                image=image, tag="TEST{0}".format(id), state="normal"
                                         )
            # rend équivalentes photos_list et photos_list_updated
            # new_list = self.photos_list_updated[:]
            self.listing_photos(self.photos_list, "normal")
            self.photos_list += self.photos_list_updated
            self.photos_list_updated = []
        else:
            print("NOTHING HAS CHANGED")
            self.listing_photos(self.photos_list, "normal")
            # for index, image in enumerate(self.photos_list):
            #     img = str(image)
            #     print(f"The index is {index}")
            #     print(f"The index of the very first image is {self.initial_img_id}")
            #     if not index:
            #         print("START")
            #         print(image)
            #         self.initial_img_id = int(''.join(list(filter(str.isdigit, img)))) - 4
            #         print(f"The new initial index for other images: {self.initial_img_id}")
            #         # print(first_img_id)
            #         print(self.canvas.itemconfigure(self.initial_img_id))
            #         self.canvas.itemconfigure(self.initial_img_id, state="normal")
            #         print("END")
            #     else:
            #         print("START FOR OTHER INDEX")
            #         print(image)
            #         self.initial_img_id += 2
            #         new_img_id = self.initial_img_id
            #         print(new_img_id)
            #         print(self.canvas.itemconfigure(new_img_id))
            #         self.canvas.itemconfigure(new_img_id, state="normal")
            #         print("END FOR OTHER INDEX")
            # toggle pour voir les photos, pas besoin de créer images
            # print(self.photos_list)

    def hide_photos_album(self, event=None):
        # print("ALL THE PICS ARE HIDDEN")
        # print(self.photos_list)
        self.listing_photos(self.photos_list, "hidden")
            # print(self.canvas.itemconfigure(5))
            # print(self.canvas.itemconfigure(7))
            # print(self.canvas.itemconfigure(9))
            # print(self.canvas.itemconfigure(11))
            # print(self.canvas.itemconfigure(13))
            # print(self.canvas.itemconfigure(15))
            # print(self.canvas.itemconfigure(5))
            # self.canvas.itemconfigure(img_id, state="hidden")
            # image_temp = self.canvas.itemcget(image)
            # print(self.canvas.itemcget(image))
            # image_state = self.canvas.itemcget(image, "state")
            # print(image_state)
            # image_state = self.canvas.cget("state")
            # print(image_state)
            # print(image_state)

            # self.changing_state_canvas_item(image_state, "hidden")

    def listing_photos(self, iterable_list, new_state):
        # num_pic_per_2_pages = 0
        for index, image in enumerate(iterable_list):
            img = str(image)
            print(f"The index is {index}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"The index of the very first image is {self.initial_img_id}")
            if not index:
                print("START")
                print(image)
                self.initial_img_id = int(''.join(list(filter(str.isdigit, img))))-4
                print(f"The new initial index for other images: {self.initial_img_id}")
                # print(first_img_id)
                print(self.canvas.itemconfigure(self.initial_img_id))
                self.changing_state_canvas_item(self.initial_img_id, new_state)
                # num_pic_per_2_pages +=1
                # if num_pic_per_2_pages == 1:
                #     self.canvas.move(self.initial_img_id, -20, -2) # coin haut gauche
                print("END")
            else:
                print("START FOR OTHER INDEX")
                print(image)
                self.initial_img_id += 2
                new_img_id = self.initial_img_id
                print(new_img_id)
                print(self.canvas.itemconfigure(new_img_id))
                self.canvas.itemconfigure(new_img_id, state=new_state)
                # num_pic_per_2_pages += 1
                # if num_pic_per_2_pages ==  2:
                #     self.canvas.move(self.initial_img_id, -200, 200) # coin bas gauche
                # elif num_pic_per_2_pages == 3:
                #     self.canvas.move(self.initial_img_id, 200, -200) # coin haut droit
                # elif num_pic_per_2_pages == 4:
                #     self.canvas.move(self.initial_img_id, 200, 200) # coin bas droit
                #     num_pic_per_2_pages = 0
                print("END FOR OTHER INDEX")

    def change_background(self, tagOrId, new_background):
        self.canvas.itemconfigure(tagOrId, image=new_background)


if __name__ == "__main__":
    # w = FullScreenWindow(root)
    App().mainloop()
