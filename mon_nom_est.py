import tkinter as tk
from tkinter import VERTICAL, HORIZONTAL
from PIL import Image, ImageTk
from images import bg_image_setup, open_image_setup_file
from fade_transition import FadeTransition
from dialog.dialog_boxes import DialogBoxes
from game_events_handler import GameEventHandler


class HomeScreen:
    def __init__(self, master):
        self.master = master
        # super().__init__(master)
        # self.config(background="black")
        self.HS_image = bg_image_setup("./images/homescreen/PA_homescreenTest.png")
        self.HSFrame = tk.Canvas(master, height=self.master.winfo_screenheight(), width=self.master.winfo_screenwidth())
        self.apply_HS_canvas_image()
        # self.grid_rowconfigure(row=0, column=1, weight=1)
        # self.grid_columnconfigure(row=1, column=0, weight=1)
        self.start_button = tk.Button(self.HSFrame, text='Jouer', width=40, command=self.intro)
        self.start_button.grid(sticky="NS")
        self.exit_game_button = tk.Button(self.HSFrame, text='Quitter', width=40, command=self.master.destroy)
        self.exit_game_button.grid()
        self.HSFrame.grid_propagate(False)
        self.HSFrame.grid()
        self.master.mainloop()


    def apply_HS_canvas_image(self):
        # print(self.HS_image)
        title_height = self.master.winfo_screenheight()/4
        title_width = self.master.winfo_screenwidth()/2
        center_height = self.master.winfo_screenheight()/2
        center_width = self.master.winfo_screenwidth()/2
        self.HSFrame.create_image(center_width, center_height, image=self.HS_image)
        self.HSFrame.create_text((title_width, title_height), text="MON NOM EST", fill="white",
                                 font=("Helvetica", 40, "bold")
        )

    def intro(self):
        self.HSFrame.grid_remove()
        self.check_game_e()

    def check_game_e(self, event=None):
        self.master.check_game_events()

    def test(self, event=None):
        print("HI!!!!")


class App(tk.Tk):
    """
    Application:
        [...]
    """
    def __init__(self):
        super().__init__()
        self.title("Mon nom est...")
        self.grid_rowconfigure(0, weight=1)  # For row 0
        self.grid_columnconfigure(0, weight=1)  # For column 0
        self.index = 2
        self.pages_name = ["room_2", "room_1", "room_0", "room1", "room2"]
        self.pages_file_location = {
            "room_2": "./images/rooms/real_rooms/bathroom/PA_SalleDeBain.png",
            "room_1": "./images/rooms/real_rooms/kitchen/PA_Cuisine.png",
            "room_0": "./images/rooms/real_rooms/main_door/PA_PorteOuverte.png",
            "room1": "./images/rooms/real_rooms/player_room/PA_CarnetDessinBureau.png",
            "room2": "./images/rooms/real_rooms/library/PA_Bibliothèque.png"
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
        self.black_background = bg_image_setup("images/intro/NB_BlackBox.png")
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
        self.fade = FadeTransition(self)
        self.dial = DialogBoxes(self)
        # self.HS = HomeScreen(self)

        # handler d'évents avec classe GameEventHandler
        self.GEH = GameEventHandler(self)
        # self.intro_ended = False

    def check_game_events(self, event=None):
        self.GEH.events_to_check()


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
        self.master.fade.create_transition()
        canvas_page = self.master.rect.change_background("app_background", self.master.pages.get(f"{room_name}"))

    def show_album(self, event=None):
        self.master.rect.open_journal()
        # self.master.dial.create_frame()
        # print("STILL THERE")


class Control(tk.Frame):
    """
    Événements gérés:
        - a: déplacement pièce à gauche
        - d: déplacement pièce à droite
        - click-gauche: appel func check events jeu (classe: GameEventHandler)
        - click-droit: prend une photo (pas encore fonctionnel)
        - middle-click: ouvre/ferme album photo (pas encore fonctionnel)
    """

    def __init__(self, master):
        super().__init__(master)
        master.bind("<a>", self.change_room_left) # aller à gauche
        master.bind("<d>", self.change_room_right) # aller à droite
        # master.bind("<Button-1>", self.master.check_game_events)
        master.bind("<Button-3>", self.take_picture) # button 3 => click droit
        master.bind("<Button-2>", self.see_album) # button 2 => mid click
        #temporaire binding
        # master.bind("<q>", self.control_change_page_left)
        # master.bind("<e>", self.control_change_page_right)

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

    def control_change_page_left(self, event=None):
        self.master.bind("<q>", self.master.rect.change_page_left)

    def control_change_page_right(self, event=None):
        self.master.bind("<e>", self.master.rect.change_page_right)


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
        # position du boutton camera à changer
        self.clickable_camera_button = self.canvas.create_image(600,300,image=self.master.camera, tag="camera_click")
        self.canvas.tag_bind(self.clickable_camera_button, "<Button-1>", self.take_camera)
        # print(self.master.camera.width(), self.master.camera.height())
        self.camera = self.canvas.create_image(self.master.winfo_screenwidth()/2, self.master.winfo_screenheight()/1.5,
                                               image=self.master.camera
                                               )
        self.album = self.canvas.create_image(self.master.winfo_screenwidth() / 2, self.master.winfo_screenheight() / 2,
                                              image=self.master.album
                                              )
        # self.canvas.itemconfigure(self.background, state="hidden")
        self.canvas.itemconfigure(self.album, state="hidden")
        self.canvas.itemconfigure(self.camera, state="hidden")
        # self.canvas.itemconfigure(self.background, state="hidden")
        # self.dialog_box = open_image_setup_file("./images/dialog/NB_BlackBarDialogBoxShrunk.png")
        self.dialog_box = open_image_setup_file("./images/intro/NB_RedBarTest.png")
        self.page_num = 1
        self.photos_list = []
        self.photos_list_updated = [] # sert à check si la liste a changé
        self.segmented_4_indexes_photos_list_updated = []
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
        # self.canvas.bind("<q>", self.change_page_left)
        # self.canvas.bind("<e>", self.change_page_right)


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

    def take_camera(self, event=None):
        # print(self.canvas.gettags("camera_click"))
        self.canvas.delete(self.clickable_camera_button)
        self.canvas.itemconfigure(self.camera, state="normal")
        # print(self.master.GEH.camera_deleted)
        self.master.GEH.camera_deleted = True
        self.master.check_game_events()
        # self.master.check_game_events()
        # print(self.canvas.gettags("camera_click"))
    def open_journal(self, event=None):
        # print("Hiiiiii I'm a canvas maker!")
        state = self.canvas.itemcget(self.album, "state")
        # print(state)
        if state == "hidden":
            # self.canvas.itemconfigure(self.album, state="normal")
            # self.canvas.lift(self.album, self.background)
            self.changing_state_canvas_item(self.album, "normal")
            # print(state)
            # self.canvas.lift(self.album)
            self.is_album_photos_updated()
            # print("I am visible!!!!!")
        elif state == "normal":
            # self.canvas.itemconfigure(self.album, state="hidden")
            self.changing_state_canvas_item(self.album, "hidden")
            # print(state)
            # self.canvas.lower(self.album)
            self.hide_photos_album()
            # print("shhhh I am hidden...")

    def changing_state_canvas_item(self, canvas_item_id, new_state):
        self.canvas.itemconfigure(canvas_item_id, state=new_state)

    def place_photo_album_list(self, crop_dimensions):
        # ajoute photo prise dans liste des photos
        image_to_crop_temp = Image.open(self.master.pages_file_location.get(self.master.pages_name[self.master.index]))
        # print(image_to_crop_temp)
        # image_to_crop_temp = self.master.pages_file_location.get(self.master.pages_name[self.master.index])
        image_to_crop = image_to_crop_temp.resize((1920,1080)).convert("RGBA")
        # image_to_crop = self.master.pages.get(self.master.pages_name[self.master.index])
        # print(image_to_crop)
        # w, h = image_to_crop.size
        # print(image_to_crop.size)
        # print(w, h)
        # print(crop_dimensions)
        pic_taken_temp = image_to_crop.crop(crop_dimensions)
        # pic_taken_temp = pic_taken_temp.convert("RGB")
        # print(pic_taken_temp)
        # pic_taken = pic_taken_temp
        # global pic_taken
        pic_taken = ImageTk.PhotoImage(pic_taken_temp)
        # print(pic_taken)
        # self.canvas.image = self.canvas.itemconfigure(pic_taken)
        # pic_taken = ImageTk.PhotoImage(image_to_crop)
        # self.photos_list_updated.append(pic_taken)
        # print(pic_taken)
        # print(pic_taken)
        # global image_id
        image_id = self.canvas.create_image(
            self.master.winfo_screenheight()/2, self.master.winfo_screenwidth()/2,
            image=pic_taken,state="hidden"
        )
        # print(image_id)
        # self.canvas.image = image_id
        # print(self.canvas.image)
        self.photos_list_updated.append(image_id)
        # print(self.photos_list)
        # print(self.photos_list_updated)
        # self.photos_list = self.photos_list_updated
        # self.photos_list_updated = []
        # print(self.photos_list)


    def is_album_photos_updated(self, event=None):
        # print(self.photos_list)
        # print(self.photos_list_updated)
        p1 = set(self.photos_list_updated)
        p2 = set(self.photos_list)
        diff = p1.difference(p2)
        # print(diff)
        if diff:
            print("SOMETHING HAS CHANGED")
            self.photos_list = self.photos_list_updated[:]
            # print(self.photos_list)
            # print(self.photos_list_updated)
            self.listing_photos()
            self.show_pics_by_page_num(self.page_num)
            "Je teste pour check si pyimage existe vraiment --> tk error sinon mais code est supposé marcher"
            # test = self.segmented_4_indexes_photos_list_updated
            # print(test)
            # for pic in test[0]:
            #     # print(pic)
            #     print(self.canvas.itemconfigure(pic)["image"][4])
        else:
            # print(self.photos_list_updated)
            print("NOTHING HAS CHANGED")
            # self.create_dialog_box()
            # print(self.segmented_4_indexes_photos_list_updated)
            # print(self.photos_list)
            # print(self.photos_list_updated)
            # print(self.segmented_4_indexes_photos_list_updated)
            if len(self.segmented_4_indexes_photos_list_updated) != 0:
                self.show_pics_by_page_num(self.page_num)


    def listing_photos(self, event=None):
        # crée image pour chaque photo dans album => grid
        self.segmented_4_indexes_photos_list_updated = []
        prev = 0
        next_segmented_index = 4
        # segmented_4_indexes_photos_list.append(self.photos_list[prev:next_segmented_index])
        # prev = next_segmented_index + 1
        # next_segmented_index += 5
        # segmented_4_indexes_photos_list.append(self.photos_list[prev:next_segmented_index])
        # print(segmented_4_indexes_photos_list)
        while len(self.photos_list[prev:next_segmented_index]) == 4:  # loop tant 4 photos par 2 pages
            pages_2 = self.photos_list[prev:next_segmented_index]
            self.segmented_4_indexes_photos_list_updated.append(pages_2)  # ajoute liste de 4 photos dans segmented_4_indexes_photos_list
            # print(segmented_4_indexes_photos_list)
            prev = next_segmented_index
            # print(prev)
            next_segmented_index += 4
            # print(next_segmented_index)
        else:
            pages_2 = self.photos_list[prev:next_segmented_index]
            if len(pages_2) != 0:
                self.segmented_4_indexes_photos_list_updated.append(pages_2)
                # print(segmented_4_indexes_photos_list)
        # print(self.segmented_4_indexes_photos_list_updated)

        # crée image pour chaque photo dans album => grid
        # print(self.photos_list)
        # print(self.photos_list_updated)
        # for image in self.photos_list_updated:
        #     print(image)
        # p1 = set(self.photos_list_updated)
        # p2 = set(self.photos_list)
        # diff = p1.difference(p2)
        # # print(diff)
        # if diff:
        #     # print(self.photos_list_updated)
        #     print("SOMETHING HAS CHANGED")
        #     # print(self.photos_list_updated)
        #     # crée image juste pour image qui se trouve dans updated list
        #     # for id, image in enumerate(self.photos_list_updated):
        #     #     print(id)
        #     #     self.canvas.create_image(self.master.winfo_screenwidth() / 2, self.master.winfo_screenheight()/2,
        #     #                                     image=image, tag="pic{0}".format(id))
        #     #
        #     for image in enumerate(self.photos_list):
        #         # img = str(image)
        #         # print(str(image))
        #         # print(int(''.join(list(filter(str.isdigit, img))))-4)
        #         # print("END")
        #         image_id = self.canvas.create_image(image=image, state="hidden")

            # rend équivalentes photos_list et photos_list_updated
            # new_list = self.photos_list_updated[:]
            # self.listing_photos(self.photos_list, "normal")
            # self.photos_list += self.photos_list_updated
            # self.photos_list_updated = []
        # else:
        #     print("NOTHING HAS CHANGED")
            # self.listing_photos(self.photos_list, "normal")
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
        pass
        # print("ALL THE PICS ARE HIDDEN")
        # print(self.photos_list)
        # self.listing_photos(self.photos_list, "hidden")
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

    # def listing_photos(self, iterable_list, new_state):
    #     num_pic_per_2_pages = 0
    #     album_frame_placement = tk.Frame(width=480, height=270, state="hidden")
    #     album_frame_placement.place(in_=self.master, anchor="c", relx=.5, rely=.5)
    #     # album_frame_placement = in_=self.master, anchor="c", relx=.5, rely=.5, background="black"
    #     for index, image in enumerate(iterable_list):
    #         img = str(image)
    #         # print(f"The index is {index}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #         # print(f"The index of the very first image is {self.initial_img_id}")
    #         if not index:
    #             print("START!!!!!!!!!!!!!!!!")
    #             print(image)
    #             self.initial_img_id = int(''.join(list(filter(str.isdigit, img))))-4
    #             # print(f"The new initial index for other images: {self.initial_img_id}")
    #             # print(first_img_id)
    #             print(self.canvas.itemconfigure(self.initial_img_id))
    #             self.changing_state_canvas_item(self.initial_img_id, new_state)
    #             num_pic_per_2_pages +=1
    #             if num_pic_per_2_pages == 1:
    #                 album_frame_placement.place(x=960, y=540, anchor="nw")
    #                 # self.canvas.move(self.initial_img_id, -20, -2) # coin haut gauche
    #                 pass
    #             print("END!!!!!!!!!!!!!!!")
    #         else:
    #             print("!!!!!!!!!!!!!!!!!START FOR OTHER INDEX")
    #             print(image)
    #             self.initial_img_id += 2
    #             new_img_id = self.initial_img_id
    #             # print(new_img_id)
    #             # print(self.canvas.itemconfigure(new_img_id))
    #             self.canvas.itemconfigure(new_img_id, state=new_state)
    #             num_pic_per_2_pages += 1
    #             if num_pic_per_2_pages ==  2:
    #                 # self.canvas.move(self.initial_img_id, -200, 200) # coin bas gauche
    #                 pass
    #             elif num_pic_per_2_pages == 3:
    #                 # self.canvas.move(self.initial_img_id, 200, -200) # coin haut droit
    #                 pass
    #             elif num_pic_per_2_pages == 4:
    #                 # self.canvas.move(self.initial_img_id, 200, 200) # coin bas droit
    #                 pass
    #                 num_pic_per_2_pages = 0
    #             print("!!!!!!!!!!!!!!!END FOR OTHER INDEX")
    #
    def change_background(self, tagOrId, new_background):
        print("L'intro a bien débuté. Background changé")
        # print(self.canvas.itemconfigure(tagOrId))
        self.canvas.itemconfigure(tagOrId, image=new_background)
        # print(self.canvas.itemconfigure(tagOrId))

    def change_page_left(self, event=None):
        # self.canvas.focus_set(event)
        print("test")
        if self.page_num > 1:
            self.page_num -= 1
            self.show_pics_by_page_num(self.page_num)

    def change_page_right(self, event=None):
        # self.canvas.focus_set(event)
        print("TEST")
        self.page_num += 1
        self.show_pics_by_page_num(self.page_num)

    def show_pics_by_page_num(self, page_num):
        """
            - for loop toutes les photos d'une page précise
            - change la clef state de toutes ces photos (hidden --> normal) et (normal --> hidden) sur ouverture album
            - max 4 photos par pages
            - change state que de 4 photos max
            - recrée une nouvelle liste index_segmented_list si joueur prend nv. photo
        """

        print("This is page {0}".format(page_num))
        index_segmented_list = page_num-1
        # print(self.segmented_4_indexes_photos_list_updated[index_segmented_list])
        if len(self.segmented_4_indexes_photos_list_updated) != 0:
            for index, pic in enumerate(self.segmented_4_indexes_photos_list_updated[index_segmented_list]):
                # print("HEY FOR LOOP")
                # print(pic)
                print(pic, index)
                # print(self.canvas.itemconfigure(pic), index)
                self.changing_state_canvas_item(pic, "normal")
                # state_key = self.canvas.itemconfigure(pic)["state"]
                # self.canvas.itemconfigure(self.canvas.itemconfigure(pic), state="normal")
                print(self.canvas.itemconfigure(pic))
                # print(self.segmented_4_indexes_photos_list_updated)
                # print(self.segmented_4_indexes_photos_list_updated[index_segmented_list])
            # print(self.segmented_4_indexes_photos_list_updated[index_segmented_list])

    def create_dialog_box(self, chosen_moment):
        """
            - crée sur demande bar dialogue + texte à display selon actions/moments joueur
            - détruit bar dialogue + texte à display après fin texte
        """

        # position black_dialog_bar
        dialog_position = (self.master.winfo_screenwidth()/2, self.master.winfo_screenheight()/1.35)
        # print(dialog_position)
        # crée barre noir dialogue
        black_dialog_bar = self.canvas.create_image(dialog_position[0], dialog_position[1], image=self.dialog_box)
        chosen_text = self.master.dial.dialog_to_use(chosen_moment) # choisit texte à display selon action/moment joueur
        # texte = positionné au centre de black_dialog_bar
        dialog_text = self.canvas.create_text((dialog_position[0],self.master.winfo_screenheight()/1.25),
                                              text="", fill="white", font=("Helvetica", 15, "italic"))
        self.master.dial.typewritten_effect(dialog_text, chosen_text)
        self.canvas.itemconfigure(black_dialog_bar, state="hidden")


# if __name__ == "__main__":
#     App().mainloop()

def main():
    root = App()
    HomeScreen(root)

if __name__ == '__main__':
    main()

