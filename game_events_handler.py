"""Classe gérant tous les intéractions + event du jeu"""
import tkinter as tk
from global_var import screen_height, screen_width
from images import bg_image_setup
from dialog.txt_files_reader import txt_files_story
from txt_story_reader import txt_story_reader, reset_story_reader


class GameEventHandler:
    """
    Conditions diff pour tt. pièces
    Conditions pour intro
    Rel.x + Rel.y
        - events_to_check
        - get_current_room_img
    """

    def __init__(self, master):
        self.master = master
        self.intro_initialized = False
        self.intro_ended = False
        self.camera_deleted = False
        self.are_rooms_visible = False
        self.rel_pos = {
            "x": 0,
            "y": 0
        }
        self.text_box = self.master.rect.canvas.create_rectangle(screen_width / 3 * 2, 0,
                                                                 screen_width, screen_height,
                                                                 fill="grey", stipple="gray50")
        self.master.rect.changing_state_canvas_item(self.text_box, "hidden")
        self.text_readable = self.master.rect.canvas.create_text(screen_width / 6 * 5, screen_height / 2,
                                                                 text="",
                                                                 fill="white", font=("Helvetica", 12, "italic"))
        self.master.rect.changing_state_canvas_item(self.text_readable, "hidden")
        self.is_desktop_visible = False
        self.is_fam_book_read = False
        self.is_pamphlet_kitchen_read = False
        self.are_dots_drawn = False

        # intéractions / widgets
        self.skip_intro_butt = tk.Button(self.master, text='Skip intro', width=40, command=self.skip_intro)

        # photos coords
        self.check_start_x = 0
        self.check_start_y = 0
        self.check_end_x = 0
        self.check_end_y = 0

        # reset val
        self.prev_and_current_room = [] # max 2 pièces

    def skip_intro(self):
        """
        Skips intro and ends the dialog
        """
        self.intro_initialized = True
        self.intro_ended = True
        self.are_rooms_visible = True
        self.skip_intro_butt.grid_remove()
        self.master.dial.stop()
        self.master.view.change_room("room_0")
        self.master.rect.changing_state_canvas_item("camera_click", "normal")
        self.master.bind("<Motion>", self.master.motion)

    def text_box_func(self):
        return self.text_box

    def text_readable_func(self):
        return self.text_readable

    def events_to_check(self):
        """
        Images:
            - pyimage 1 = toilettes
            - pyimage 2 = cuisine
                - pyimage 6 = cuisine (orange)
                - pyimage 7 = cuisine (tiroir)
            - pyimage 3 = salle principale (porte)
            - pyimage 4 = chambre dessin
                - pyimage 8 = close-up cahier dessin
            - pyimage 5 = bibliothèque
                - pyimage 10 = close-up livres
                    - pyimage 11 = lire livre famille
            - pyimage 22 = cuisine changée
        """
        # print(self.has_room_changed)
        current_room = self.get_current_room_img()
        if not self.intro_initialized and not self.intro_ended:
            # DialogBoxes().dialog_to_use("intro")
            print("INTRO COMMENCE")
            # windll.user32.BlockInput(True)
            # enlève souris input, click et intéractions avec clavier
            self.master.rect.change_background("app_background", self.master.black_background)
            self.skip_intro_butt.grid()
            # self.master.rect.canvas.itemconfigure(self.master.rect.camera, state="hidden")
            self.master.rect.create_dialog_box("intro")
            # print("EN ATTENTE")
            self.intro_initialized = True
        elif self.intro_initialized and not self.intro_ended:
            self.intro_ended = True
            self.master.view.change_room("room_0")
        elif not self.are_rooms_visible:
            # print("Je me réveille...")
            self.master.rect.changing_state_canvas_item("camera_click", "normal")
            self.master.rect.create_dialog_box("réveil")
            self.are_rooms_visible = True
            # windll.user32.BlockInput(False)
            # Bouger la souris réappelle func motion de classe App
            self.master.bind("<Motion>", self.master.motion)
        elif current_room == "pyimage1":
            pass
        elif current_room == "pyimage2":
            # print(self.master.pages_file_location["room_1"])
            if 575 < self.rel_pos.get("x") < 1000 and 0 < self.rel_pos.get("y") < 300:
                self.master.pages["room_1"] = bg_image_setup("./images/rooms/changed_rooms/kitchen/PA_CH_Cuisine.png")
                self.master.fade.create_transition()
                self.master.rect.change_background("app_background",
                                                   self.master.pages.get("room_1"))
        elif current_room in {"pyimage23", "pyimage24"}:
            if 0 < self.rel_pos.get("x") < 500 and 500 < self.rel_pos.get("y") < 650:
                self.master.rect.orange_kitchen.show_tip(self.rel_pos)
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.change_background("app_background",
                                                                              self.master.kitchen_closeup.get(
                                                                                  "oranges")))
            elif 800 < self.rel_pos.get("x") < 1385 and 0 < self.rel_pos.get("y") < 210:
                self.master.rect.drawer_open.show_tip(self.rel_pos)
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.change_background("app_background",
                                                                              self.master.kitchen_closeup.get(
                                                                                  "drawer")))
            else:
                self.master.rect.orange_kitchen.hide_tip()
                self.master.rect.drawer_open.hide_tip()
        elif current_room == "pyimage6":
            # -15, 230
            x_range = 15
            # 180, 630
            y_range = 600
            if x_range - 30 < self.check_start_x < self.check_end_x < x_range + 1525 \
                    and y_range - 420 < self.check_start_y < self.check_end_y < y_range + 30:
                print("Preuves pour activités paranormales.")
                self.master.rect.create_dialog_box("preuve_parnm_oranges")
        elif current_room == "pyimage7":
            if 250 < self.rel_pos.get("x") < 625 and 650 < self.rel_pos.get("y") < 725:
                self.master.rect.read_pamphlet_drawer.show_tip(self.rel_pos)
                if not self.is_pamphlet_kitchen_read:
                    self.master.bind("<e>",
                                     lambda x: txt_story_reader(self.master,
                                                                "./dialog/dialog_text/lire_brochure_cuisine.txt"))
                self.is_pamphlet_kitchen_read = True
            else:
                self.master.rect.read_pamphlet_drawer.hide_tip()
        elif current_room == "pyimage3":
            self.master.rect.changing_state_canvas_item("camera_click", "normal")
            if self.camera_deleted:
                print("SALUT C'EST MOI LA CAMERA")
                self.master.rect.create_dialog_box("camera_trouvee")
                # évite de retoggle cette partie du code. iImage "pickable caméra" = détruite
                self.camera_deleted = False
        elif current_room == "pyimage4":
            if 575 < self.rel_pos.get("x") < 1000 and 565 < self.rel_pos.get("y") < 650:
                print("DESSIN")
                print(f"x: {self.rel_pos.get('x')}, y: {self.rel_pos.get('y')}")
                self.master.rect.popup_draw.show_tip(self.rel_pos)
                # print(pygame.mouse.get_pressed())
                # print(pygame.mouse.get_pressed()[0])
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.change_background("app_background",
                                                                              self.master.desktop_closeup.get(
                                                                                  "desktop")))
            else:
                self.master.rect.popup_draw.hide_tip()
        elif current_room == "pyimage8":
            if 340 < self.rel_pos.get("x") < 1125 and 380 < self.rel_pos.get("y") < 825:
                print("DESSINEEEER")
                print(f"x: {self.rel_pos.get('x')}, y: {self.rel_pos.get('y')}")
                self.master.rect.draw.show_tip(self.rel_pos)
                self.master.bind("<e>",
                                 lambda x: self.master.rect.change_background("app_background",
                                                                              self.master.desktop_closeup.get(
                                                                                  "draw")))
            else:
                self.master.rect.draw.hide_tip()
        elif current_room == "pyimage9":
            if not self.are_dots_drawn:
                self.master.dots.place_dots(self.master.dots.
                                            get_connect_dots_position("./images/connect the dots/FishConnectDots.png"))
                self.master.rect.canvas.bind("<Button-1>",
                                             lambda x: self.master.dots.get_x_y(self.rel_pos))
                self.master.rect.canvas.bind("<B1-Motion>",
                                             lambda x: self.master.dots.paint(self.rel_pos))
                self.are_dots_drawn = True
        elif current_room == "pyimage5":
            if 800 < self.rel_pos.get("x") < 1000 and 50 < self.rel_pos.get("y") < 250:
                print("Livres ???!!!")
                self.master.rect.see_books.show_tip(self.rel_pos)
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.change_background("app_background",
                                                                              self.master.library_closeup.get(
                                                                                  "see_books")))
            else:
                self.master.rect.see_books.hide_tip()
        # regarde livres dispo
        elif current_room == "pyimage10":
            print("Accès à tous les livres...")
            if 380 < self.rel_pos.get("x") < 480:
                print("LIVRE A LIRE")
                self.master.rect.open_family_book.show_tip(self.rel_pos)
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.change_background("app_background",
                                                                              self.master.library_closeup.get(
                                                                                  "family_book")))
            else:
                self.master.rect.open_family_book.hide_tip()
        # joueur lit livre "famille"
        elif current_room == "pyimage11":
            print(self.is_fam_book_read)
            if not self.is_fam_book_read:
                print(txt_files_story("./dialog/dialog_text/lire_livre.txt"))
                txt_story_reader(self.master, "./dialog/dialog_text/lire_livre.txt")
            self.is_fam_book_read = True
        if not current_room == "pyimage3" and not self.camera_deleted:
            self.master.rect.changing_state_canvas_item("camera_click", "hidden")
        else:
            # print("Rien à signaler...")
            pass

    def get_current_room_img(self):
        """
        Return n° pyimage actuelle (image fond d'écran)
        """
        # bg = self.master.rect.get_bg_att()
        # print(bg)
        current_bg = self.master.rect.get_key_val_canvas_obj("app_background", "image")
        if len(self.prev_and_current_room) == 0:
            self.prev_and_current_room.append(current_bg)
        elif self.prev_and_current_room[0] != current_bg and len(self.prev_and_current_room) == 1:
            self.prev_and_current_room.append(current_bg)
        elif len(self.prev_and_current_room) == 2:
            if self.prev_and_current_room[1] != current_bg:
                self.prev_and_current_room.pop(0)
                self.prev_and_current_room.append(current_bg)
        # print(self.master.rect.get_key_val_canvas_obj("app_background", "image"))
        # print(self.prev_and_current_room)
        # print(self.prev_and_current_room)
        self.reset_val()
        return self.master.rect.get_key_val_canvas_obj("app_background", "image")  # background

    def reset_val(self):
        """
        5 conditions principales:
            - toilette
            - cuisine
            - porte principale
            - bureau
            - biblithèque
        conditions secondaires:
            - ...
        """
        # print("test pour func reset val")
        # print(self.prev_and_current_room)
        self.master.unbind("<Button-1>")
        prev_room = self.prev_and_current_room[0]
        current_room = ""
        if len(self.prev_and_current_room) > 1:
            # print(self.prev_and_current_room)
            current_room = self.prev_and_current_room[1]
        print(self.prev_and_current_room)
        # porte principale --> cuisine OU bureau
        if prev_room == "pyimage3" and current_room in {"pyimage2", "pyimage4"}:
            print("1")
            pass
        # cuisine --> toilette OU porte principale
        elif prev_room in {"pyimage24", "pyimage24"} and current_room in {"pyimage1", "pyimage3"}:
            print("2")
            self.master.rect.orange_kitchen.hide_tip()
            self.master.rect.drawer_open.hide_tip()
        # cuisine --> oranges
        elif prev_room in {"pyimage23", "pyimage24"} and current_room == "pyimage6":
            print("4 condition")
            self.master.rect.orange_kitchen.hide_tip()
        # cuisine --> brochure
        elif prev_room in {"pyimage23", "pyimage24"} and current_room == "pyimage7":
            print("3 condition")
            self.master.rect.drawer_open.hide_tip()
        # brochure --> toilette OU porte principale
        elif prev_room == "pyimage7" and current_room in {"pyimage1", "pyimage3"}:
            print("5 condition")
            self.master.rect.read_pamphlet_drawer.hide_tip()
            self.is_pamphlet_kitchen_read = False
            reset_story_reader(self.master)
        # bureau --> porte principale OU bibliothèque
        elif prev_room == "pyimage4" and current_room in {"pyimage3", "pyimage5"}:
            print("6 condition")
            self.master.rect.popup_draw.hide_tip()
        # bureau --> cahier dessin
        elif prev_room == "pyimage4" and current_room == "pyimage8":
            print("7 condition")
            self.master.rect.popup_draw.hide_tip()
        # cahier dessin --> porte principale OU bureau
        elif prev_room == "pyimage8" and current_room in {"pyimage3", "pyimage5"}:
            self.master.rect.draw.hide_tip()
        # cahier dessin --> dessiner
        elif prev_room == "pyimage8" and current_room == "pyimage9":
            self.master.rect.draw.hide_tip()
        # dessiner --> porte principale OU bibliothèque
        elif prev_room == "pyimage9" and current_room in {"pyimage3", "pyimage5"}:
            self.master.rect.canvas.unbind("<Button-1>")
            self.master.rect.canvas.unbind("<B1-Motion>")
            self.master.dots.reset()
            self.are_dots_drawn = False
        # bibliothèque --> bureau
        elif prev_room == "pyimage5" and current_room == "pyimage4":
            self.master.rect.see_books.hide_tip()
        # bibliothèque --> close-up livres dispo
        elif prev_room == "pyimage5" and current_room == "pyimage10":
            self.master.rect.see_books.hide_tip()
        # close-up livres dispo --> bureau
        elif prev_room == "pyimage10" and current_room == "pyimage4":
            self.master.rect.open_family_book.hide_tip()
        # close-up livres dispo --> lire livre famille
        elif prev_room == "pyimage10" and current_room == "pyimage11":
            self.master.rect.open_family_book.hide_tip()
        # lire livre famille --> bureau
        elif prev_room == "pyimage11" and current_room == "pyimage4":
            self.master.rect.open_family_book.hide_tip()
            self.is_fam_book_read = False
            reset_story_reader(self.master)
        else:
            print("c'est quoi ce foutoir..")
