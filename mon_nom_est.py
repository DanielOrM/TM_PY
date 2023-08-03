import tkinter as tk
from tkinter import VERTICAL, HORIZONTAL
from PIL import Image, ImageTk
from images import bg_image_setup, open_image_setup_file
from fade_transition import FadeTransition
from dialog.dialog_boxes import DialogBoxes
from game_events_handler import GameEventHandler
from hover_message import create_hover_message, HoverMessRelPos
from global_var import screen_width, screen_height
import pygame
import pynput


class HomeScreen:
    def __init__(self, master):
        self.master = master
        self.mouse_listener = pynput.mouse.Listener(suppress=True)
        self.keyboard_listener = pynput.mouse.Listener(suppress=True)
        # super().__init__(master)
        # self.config(background="black")
        # configure de grid pour le reste du code
        self.master.grid_rowconfigure(0, weight=1)  # For row 0
        self.master.grid_columnconfigure(0, weight=1)  # For column 0
        self.HS_image = bg_image_setup("./images/homescreen/PA_homescreenTest.png")
        self.HSFrame = tk.Canvas(master, height=screen_height, width=screen_width)
        self.apply_HS_canvas_image()
        self.start_button = tk.Button(self.HSFrame, text='Jouer', width=40, command=self.intro)
        self.start_button.grid()
        self.exit_game_button = tk.Button(self.HSFrame, text='Quitter', width=40, command=self.master.destroy)
        self.exit_game_button.grid()
        self.HSFrame.grid_propagate(False)
        self.HSFrame.grid()
        pygame.mixer.music.load("./son/DARKNESS.mp3")
        pygame.mixer.music.play()
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
        # rend l'écran d'accueil accessible à partir de master
        self.master.HS = self.HSFrame

    def intro(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
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
        # self.grid_rowconfigure(0, weight=1)  # For row 0
        # self.grid_columnconfigure(0, weight=1)  # For column 0
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
        self.left_arrow = open_image_setup_file("./images/player/red_arrow_left.png").subsample(16, 16)
        self.right_arrow = open_image_setup_file("./images/player/red_arrow_right.png").subsample(16, 16)
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

        # obtenir coords souris
        # self.bind("<Motion>", self.motion)

        # HS widget
        self.HS = None

    def check_game_events(self, event=None):
        self.GEH.events_to_check()

    def motion(self, event):
        self.GEH.rel_pos["x"], self.GEH.rel_pos["y"] = event.x, event.y
        print("{}, {}".format(self.GEH.rel_pos["x"], self.GEH.rel_pos["y"])) # coords en x et en y de la souris
        self.check_game_events()


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
        # print(self.canvas.itemconfigure(self.clickable_camera_button))
        self.is_hover_message_running = False
        # messages intéractions
        create_hover_message(self.master, self.canvas, self.clickable_camera_button, text="[Click Gauche]") # prendre caméra
        self.popup_draw = HoverMessRelPos(self.master, self.canvas, "[Click gauche] pour dessiner")
        self.canvas.tag_bind(self.clickable_camera_button, "<Button-1>", self.take_camera)
        # print(self.master.camera.width(), self.master.camera.height())
        self.camera = self.canvas.create_image(self.master.winfo_screenwidth()/2, self.master.winfo_screenheight()/1.5,
                                               image=self.master.camera
                                               )
        self.album = self.canvas.create_image(self.master.winfo_screenwidth() / 2, self.master.winfo_screenheight() / 2,
                                              image=self.master.album
                                              )
        self.change_page_to_left_arrow = self.canvas.create_image(560, 560,
                                              image=self.master.left_arrow, state="hidden"
                                            )
        self.change_page_to_right_arrow = self.canvas.create_image(975, 560,
                                              image=self.master.right_arrow, state="hidden"
                                            )
        self.canvas.tag_bind(self.change_page_to_left_arrow, "<Button-1>", self.change_page_left)
        self.canvas.tag_bind(self.change_page_to_right_arrow, "<Button-1>", self.change_page_right)
        self.images_pic_reference = []
        # self.canvas.itemconfigure(self.background, state="hidden")
        self.canvas.itemconfigure("camera_click", state="hidden")
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

    def hightlight_items(self, image, event=None):
        print(self.canvas.itemconfigure(self.clickable_camera_button))
        # self.canvas.itemconfigure(image, activeimage="yellow")

    def take_camera(self, event=None):
        # print(self.canvas.gettags("camera_click"))
        self.canvas.delete(self.clickable_camera_button)
        self.canvas.itemconfigure(self.camera, state="normal")
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
            self.changing_state_canvas_item(self.change_page_to_left_arrow, "normal")
            self.changing_state_canvas_item(self.change_page_to_right_arrow, "normal")
            # print(state)
            # self.canvas.lift(self.album)
            self.is_album_photos_updated()
            self.show_pics_by_page_num(self.page_num)
            # print("I am visible!!!!!")
        elif state == "normal":
            # self.canvas.itemconfigure(self.album, state="hidden")
            self.changing_state_canvas_item(self.album, "hidden")
            self.changing_state_canvas_item(self.change_page_to_left_arrow, "hidden")
            self.changing_state_canvas_item(self.change_page_to_right_arrow, "hidden")
            # print(state)
            # self.canvas.lower(self.album)
            self.hide_photos_album()
            # print("shhhh I am hidden...")

    def changing_state_canvas_item(self, canvas_item_id, new_state):
        self.canvas.itemconfigure(canvas_item_id, state=new_state)

    def change_is_running_value(self):
        self.is_hover_message_running = not self.is_hover_message_running

    def place_photo_album_list(self, crop_dimensions):
        # ajoute photo prise dans liste des photos
        image_to_crop_temp = Image.open(self.master.pages_file_location.get(self.master.pages_name[self.master.index]))
        image_to_crop = image_to_crop_temp.resize((screen_width,screen_height)).convert("RGBA")
        # resize pour que photo ait assez de place dans album
        # print(screen_width/8)
        # print(screen_height/16)
        pic_size_in_album = (int(screen_width/8), int(screen_height/7))
        print(pic_size_in_album)
        pic_taken_temp = image_to_crop.crop(crop_dimensions).resize(pic_size_in_album)
        pic_taken = ImageTk.PhotoImage(pic_taken_temp, master=self.master)
        self.images_pic_reference.append(pic_taken)
        image_id = self.canvas.create_image(
            0, 0,
            image=pic_taken,state="hidden"
        )
        self.photos_list_updated.append(image_id)

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
            self.listing_photos()
        else:
            print("NOTHING HAS CHANGED")

    def listing_photos(self, event=None):
        # crée image pour chaque photo dans album => grid
        max_num_pics = 4
        self.segmented_4_indexes_photos_list_updated=[self.photos_list[i:i + max_num_pics] for i in range(0, len(self.photos_list), max_num_pics)]
        print(self.segmented_4_indexes_photos_list_updated)

    def change_background(self, tagOrId, new_background):
        print("L'intro a bien débuté. Background changé")
        # print(self.canvas.itemconfigure(tagOrId))
        self.canvas.itemconfigure(tagOrId, image=new_background)
        # print(self.canvas.itemconfigure(tagOrId))

    def change_page_left(self, event=None):
        # self.canvas.focus_set(event)
        print("test")
        if self.page_num > 1:
            self.hide_photos_album()
            self.page_num -= 1
            self.is_album_photos_updated()
            self.show_pics_by_page_num(self.page_num)

    def change_page_right(self, event=None):
        # self.canvas.focus_set(event)
        print("TEST")
        self.hide_photos_album()
        self.page_num += 1
        self.is_album_photos_updated()
        self.show_pics_by_page_num(self.page_num)

    def get_bg_att(self, event=None):
        # return "canvas object" avec le tag "app_background"
        return self.canvas.itemconfigure("app_background")

    def get_key_val_canvas_obj(self, obj, key):
        return self.canvas.itemcget(obj, key)

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
            try:
                current_pics_on_album = self.segmented_4_indexes_photos_list_updated[index_segmented_list]
                for index, pic in enumerate(current_pics_on_album):
                    # print("HEY FOR LOOP")
                    # print(pic)
                    print(pic, index)
                    # print(self.canvas.itemconfigure(pic), index)
                    if index == 0:
                        print("premier")
                        relx = int(screen_width/2.36)
                        rely = int(screen_height/2.65)
                        self.canvas.moveto(pic, relx, rely)
                    elif index == 1:
                        print("deuxième")
                        relx = int(screen_width/1.71)
                        rely = int(screen_height/2.65)
                        self.canvas.moveto(pic, relx, rely)
                    elif index == 2:
                        print("troisième")
                        relx = int(screen_width / 2.36)
                        rely = int(screen_height/1.82)
                        self.canvas.moveto(pic, relx, rely)
                    elif index == 3:
                        print("quatrième")
                        relx = int(screen_width / 1.71)
                        rely = int(screen_height / 1.82)
                        self.canvas.moveto(pic, relx, rely)
                    self.changing_state_canvas_item(pic, "normal")
                    print(self.canvas.itemcget(pic, "state"))
            except IndexError:
                print("Il n'y a pas encore de nouvelles images...")
                # state_key = self.canvas.itemconfigure(pic)["state"]
                # self.canvas.itemconfigure(self.canvas.itemconfigure(pic), state="normal")
                # print(self.canvas.itemconfigure(pic))
                # print(self.segmented_4_indexes_photos_list_updated)
                # print(self.segmented_4_indexes_photos_list_updated[index_segmented_list])
            # print(self.segmented_4_indexes_photos_list_updated[index_segmented_list])

    def hide_photos_album(self, event=None):
        # print("J'étais normal et maintenant je suis invisible")
        index_list = self.page_num-1
        print(index_list)
        if len(self.segmented_4_indexes_photos_list_updated) != 0:
            try:
                for pic in self.segmented_4_indexes_photos_list_updated[index_list]:
                    self.changing_state_canvas_item(pic, "hidden")
                    print(self.canvas.itemcget(pic, "state"))
            except IndexError:
                pass

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
    pygame.mixer.init()
    root = App()
    HomeScreen(root)


if __name__ == '__main__':
    main()


