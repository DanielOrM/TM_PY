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
        """unbind tous les <Button-1> pour éviter:
        click n'importe où --> close-up"""
        self.master.unbind("<Button-1>")  # temporaire --> reset_val++efficace
        self.reset_val()
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
        elif self.get_current_room_img() == "pyimage1":
            pass
        elif self.get_current_room_img() == "pyimage2":
            # print(self.master.pages_file_location["room_1"])
            if 575 < self.rel_pos.get("x") < 1000 and 0 < self.rel_pos.get("y") < 300:
                self.master.pages["room_1"] = bg_image_setup("./images/rooms/changed_rooms/kitchen/PA_CH_Cuisine.png")
                self.master.fade.create_transition()
                self.master.rect.change_background("app_background",
                                                   self.master.pages.get("room_1"))
        elif self.get_current_room_img() == "pyimage23" or self.get_current_room_img() == "pyimage24":
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
        elif self.get_current_room_img() == "pyimage6":
            # cacher mess pop-up CUISINE
            self.master.rect.orange_kitchen.hide_tip()
            self.master.rect.drawer_open.hide_tip()
            # -15, 230
            x_range = 15
            # 180, 630
            y_range = 600
            if x_range - 30 < self.check_start_x < self.check_end_x < x_range + 1525 \
                    and y_range - 420 < self.check_start_y < self.check_end_y < y_range + 30:
                print("Preuves pour activités paranormales.")
                self.master.rect.create_dialog_box("preuve_parnm_oranges")
        elif self.get_current_room_img() == "pyimage7":
            # cacher mess pop-up CUISINE
            self.master.rect.orange_kitchen.hide_tip()
            self.master.rect.drawer_open.hide_tip()
            if 250 < self.rel_pos.get("x") < 625 and 650 < self.rel_pos.get("y") < 725:
                self.master.rect.read_pamphlet_drawer.show_tip(self.rel_pos)
                if not self.is_pamphlet_kitchen_read:
                    self.master.bind("<e>",
                                     lambda x: txt_story_reader(self.master,
                                                                "./dialog/dialog_text/lire_brochure_cuisine.txt"))
                self.is_pamphlet_kitchen_read = True
            else:
                self.master.rect.read_pamphlet_drawer.hide_tip()
        elif self.get_current_room_img() == "pyimage3":
            # lire brochure cuisine
            self.is_pamphlet_kitchen_read = False
            # cacher mess pop-up CUISINE
            self.master.rect.orange_kitchen.hide_tip()
            self.master.rect.drawer_open.hide_tip()
            self.master.rect.read_pamphlet_drawer.hide_tip()
            # cacher mess pop-up BUREAU
            self.master.rect.popup_draw.hide_tip()
            reset_story_reader(self.master)
            self.master.rect.changing_state_canvas_item("camera_click", "normal")
            if self.camera_deleted:
                print("SALUT C'EST MOI LA CAMERA")
                self.master.rect.create_dialog_box("camera_trouvee")
                # évite de retoggle cette partie du code. iImage "pickable caméra" = détruite
                self.camera_deleted = False
        elif self.get_current_room_img() == "pyimage4":
            # pour pyimage 11 (lire)
            self.is_fam_book_read = False
            reset_story_reader(self.master)
            # cacher mess pop-up BIBLIOTHEQUE
            self.master.rect.see_books.hide_tip()
            self.master.rect.open_family_book.hide_tip()
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
        elif self.get_current_room_img() == "pyimage8":
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
        elif self.get_current_room_img() == "pyimage9":
            if not self.are_dots_drawn:
                self.master.dots.place_dots(self.master.dots.
                                            get_connect_dots_position("./images/connect the dots/FishConnectDots.png"))
                self.master.rect.canvas.bind("<Button-1>",
                                             lambda x: self.master.dots.get_x_y(self.rel_pos))
                self.master.rect.canvas.bind("<B1-Motion>",
                                             lambda x: self.master.dots.paint(self.rel_pos))
                self.are_dots_drawn = True
        elif self.get_current_room_img() == "pyimage5":
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
        elif self.get_current_room_img() == "pyimage10":
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
        elif self.get_current_room_img() == "pyimage11":
            # print(self.rel_pos)
            # self.master.rect.read_fam_book.show_tip(self.rel_pos)
            # quand joueur appuie sur E, ouvre image "read_fam_book" et enlève le texte affiché
            # self.master.bind("<E>", lambda x: self.master.rect.change_background("app_background", self.master.library_closeup.get("read_fam_book")), self.master.rect.read_fam_book.hide_tip())
            # self.master.bind("<e>", lambda x: self.master.rect.change_background("app_background", self.master.library_closeup.get("read_fam_book")))
            # self.master.bind("<e>", lambda x: self.master.rect.change_background("app_background",
            #                                                                      self.master.library_closeup.get(
            #                                                                          "read_fam_book")))
            print(self.is_fam_book_read)
            if not self.is_fam_book_read:
                print(txt_files_story("./dialog/dialog_text/lire_livre.txt"))
                txt_story_reader(self.master, "./dialog/dialog_text/lire_livre.txt")
                # self.master.rect.canvas.create_rectangle(screen_width / 3 * 2, 0,
                #                                          screen_width, screen_height, fill="grey", stipple="gray50")
                # self.master.rect.canvas.create_text(screen_width / 6 * 5, screen_height / 2,
                #                                     text=txt_files_story("./dialog/dialog_text/lire_livre.txt"),
                #                                     fill="white", font=("Helvetica", 12, "italic"))

                # self.master.rect.canvas.create_text(screen_width/6*5, screen_height/4,
                #                                     text=txt_files_reader("./dialog/dialog_text/lire_livre.txt"),
                #                                     fill="white", font=("Helvetica", 12, "italic"),
                #                                     justify="left")
                # text=txt_files_reader("./dialog/dialog_text/lire_livre.txt")
            self.is_fam_book_read = True
        if not self.get_current_room_img() == "pyimage3" and not self.camera_deleted:
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
        # print(self.master.rect.get_key_val_canvas_obj("app_background", "image"))
        return self.master.rect.get_key_val_canvas_obj("app_background", "image")  # background

    def reset_val(self):
        # cacher mess pop-up BUREAU (pyimage4)
        if self.get_current_room_img() == "pyimage4":
            self.master.rect.popup_draw.hide_tip()
        # lire brochure cuisine (pyimage7)
        if self.get_current_room_img() != "pyimage7":
            self.is_pamphlet_kitchen_read = False
            reset_story_reader(self.master)
        # cacher mess pop-up CUISINE (pyimage2)
        if self.get_current_room_img() != "pyimage2":
            self.master.rect.orange_kitchen.hide_tip()
            self.master.rect.drawer_open.hide_tip()
            self.master.rect.read_pamphlet_drawer.hide_tip()
        # connect the dots
        elif self.get_current_room_img() != "pyimage9":
            self.master.rect.canvas.unbind("<Button-1>")
            self.master.rect.canvas.unbind("<B1-Motion>")
            self.master.dots.reset()
            self.are_dots_drawn = False
