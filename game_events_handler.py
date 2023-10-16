"""Classe gérant tous les intéractions + event du jeu"""
import tkinter as tk
from global_var import screen_height, screen_width
from images import bg_image_setup
from son.channels import pen_channel
from son.random_sound_effects import play_sound_effect, set_interval
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
        self.is_camera_available = False
        self.are_rooms_visible = False
        self.rel_pos = {
            "x": 0,
            "y": 0
        }
        self.text_box = self.master.rect.canvas.create_rectangle(screen_width / 3 * 2, 0,
                                                                 screen_width, screen_height,
                                                                 fill="grey", stipple="gray50")
        self.master.rect.changing_state_canvas_item(self.text_box, "hidden")
        self.text_readable = self.master.rect.canvas.create_text(
            screen_width / 6 * 5, screen_height / 2,
            text="",
            fill="white",
            font=("Helvetica", 12, "italic"))
        self.master.rect.changing_state_canvas_item(self.text_readable, "hidden")
        self.is_desktop_visible = False
        self.is_fam_book_read = False
        self.is_pamphlet_kitchen_read = False
        self.are_dots_drawn = False
        self.has_monster_appeared = False
        self.is_door_dial_1_running = False
        self.is_door_dial_2_running = False
        self.is_player_room_entered = False
        self.is_drawing_book_discovered = False
        self.are_drawings_discovered = False
        self.are_randm_sound_activated = False

        # intéractions / widgets
        self.skip_intro_butt = tk.Button(self.master,
                                         text="Passer l'introduction", width=40, command=self.skip_intro)

        # intéractions porte principale
        self.door_try = 0

        # photos coords
        self.check_start_x = 0
        self.check_start_y = 0
        self.check_end_x = 0
        self.check_end_y = 0

        # reset val
        self.prev_and_current_room = []  # max 2 pièces

        # dots
        self.index_dot = 0
        self.img_list = ["./images/connect the dots/FishDrawnDotsSize.png",
                         "./images/connect the dots/DotsCat.png",
                         "./images/connect the dots/DotsWolfSide.png",
                         "./images/connect the dots/DotsWerewolf.png",
                         "./images/connect the dots/DotsInkAlien.png"
                         ]
        # self.img_list = ["./images/connect the dots/DotsInkAlien.png"]

    def skip_intro(self):
        """
        Skips intro and ends the dialog
        """
        self.intro_initialized = True
        self.intro_ended = True
        self.are_rooms_visible = True
        self.skip_intro_butt.grid_remove()
        self.master.dial.stop()
        self.master.view.simple_transition("room_0")
        # self.master.view.change_room("room_0")
        self.master.game_controls.initialize_controls()
        self.master.rect.changing_state_canvas_item("camera_click", "normal")
        self.master.bind("<Motion>", self.master.motion)

    def events_to_check(self):
        """
        Images:
            - pyimage 1 = toilettes
            - pyimage 2 = cuisine
                - pyimage 6 = cuisine (orange)
                - pyimage 7 = cuisine (tiroir)
            - pyimage 3 = salle principale (porte)
            - pyimage 4 = chambre dessin
                - pyimage 9 = close-up cahier dessin
            - pyimage 5 = bibliothèque
                - pyimage 10 = close-up livres
                    - pyimage 11 = lire livre famille
            - pyimage 25/26 = cuisine changée
        Close-up:
            - 6, 7, 8, 9, 10, 11
        """
        current_room = self.get_current_room_img()
        if not self.intro_initialized and not self.intro_ended:
            # enlève souris input, click et intéractions avec clavier
            self.master.rect.change_background("app_background", self.master.black_background)
            self.skip_intro_butt.grid()
            self.master.rect.create_dialog_box("intro")
            self.intro_initialized = True
        elif self.intro_initialized and not self.intro_ended:
            self.intro_ended = True
            self.skip_intro_butt.grid_remove()
            self.master.view.simple_transition("room_0")
            self.master.game_controls.initialize_controls()
        elif not self.are_rooms_visible:
            self.master.rect.changing_state_canvas_item("camera_click", "normal")
            self.master.rect.create_dialog_box("réveil")
            self.are_rooms_visible = True
            # Bouger la souris réappelle func motion de classe App
            self.master.bind("<Motion>", self.master.motion)
        elif current_room == "pyimage1":
            pass
        # print("Preuves pour activités paranormales.")
        elif current_room == "pyimage2":
            if screen_width / (1536 / 575) < self.rel_pos.get("x") < screen_width / (192 / 125) \
                    and 0 < self.rel_pos.get("y") < screen_height / (72 / 25):
                self.master.pages["room_1"] = \
                    bg_image_setup("./images/rooms/changed_rooms/kitchen/PA_CH_Cuisine.png")
                self.master.view.simple_transition("room_1")
        elif current_room in {"pyimage25", "pyimage26"}:
            if 0 < self.rel_pos.get("x") < screen_width / (384 / 125) < self.rel_pos.get("y") < screen_height / (
                    432 / 325):
                self.master.rect.orange_kitchen.show_tip(self.rel_pos)
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.
                                 change_background("app_background",
                                                   self.master.kitchen_closeup.get("oranges")))
            elif screen_width / (48 / 25) < self.rel_pos.get("x") < screen_width / (11 / 10) \
                    and 0 < self.rel_pos.get("y") < screen_height / (144 / 35):
                self.master.rect.drawer_open.show_tip(self.rel_pos)
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.
                                 change_background("app_background",
                                                   self.master.kitchen_closeup.get("drawer")))
            else:
                self.master.rect.orange_kitchen.hide_tip()
                self.master.rect.drawer_open.hide_tip()
        elif current_room == "pyimage6":
            # -15, 1540
            x_l_tol = screen_width / (-512 / 5)
            x_r_tol = screen_width / (384 / 385)
            # 180, 630
            y_l_tol = screen_height / (24 / 5)
            y_r_tol = screen_height / (48 / 35)
            if x_l_tol < self.check_start_x < self.check_end_x < x_r_tol \
                    and y_l_tol < self.check_start_y < self.check_end_y < y_r_tol:
                # action paranm.
                self.master.rect.create_dialog_box("preuve_parnm_oranges")
        elif current_room == "pyimage7":
            # 250, 625
            x_l_tol = screen_width / (768 / 125)
            x_r_tol = screen_width / (1536 / 625)
            # 650, 725
            y_l_tol = screen_height / (432 / 325)
            y_r_tol = screen_height / (864 / 725)
            if x_l_tol < self.rel_pos.get("x") < x_r_tol \
                    and y_l_tol < self.rel_pos.get("y") < y_r_tol:
                self.master.rect.read_pamphlet_drawer.show_tip(self.rel_pos)
                if not self.is_pamphlet_kitchen_read:
                    self.master.bind("<e>",
                                     lambda x: txt_story_reader(self.master,
                                                                "./dialog/dialog_text/lire_brochure_cuisine.txt"))
                self.is_pamphlet_kitchen_read = True
            else:
                self.master.rect.read_pamphlet_drawer.hide_tip()
        elif current_room == "pyimage3":
            if not self.are_randm_sound_activated:
                self.are_randm_sound_activated = True
                set_interval(play_sound_effect, 300)
            # 1050, 1100
            x_l_tol = screen_width / (256 / 175)
            x_r_tol = screen_width / (384 / 275)
            # 430, 470
            y_l_tol = screen_height / (432 / 215)
            y_r_tol = screen_height / (432 / 235)
            if x_l_tol < self.rel_pos.get("x") < x_r_tol \
                    and y_l_tol < self.rel_pos.get("y") < y_r_tol:
                self.master.rect.door_handle.show_tip(self.rel_pos)
                self.master.bind("<Button-1>", self.incr_door_try)
                if self.door_try == 1:
                    if not self.is_door_dial_1_running:
                        self.is_door_dial_1_running = True
                        self.master.rect.create_dialog_box("porte_essai")
                elif self.door_try == 2:
                    if not self.is_door_dial_2_running:
                        self.is_door_dial_2_running = True
                        self.master.rect.create_dialog_box("porte_essai_2")
            else:
                self.master.rect.door_handle.hide_tip()
            self.master.rect.changing_state_canvas_item("camera_click", "normal")
            if self.camera_deleted:
                self.master.rect.create_dialog_box("camera_trouvee")
                # évite de retoggle cette partie du code. Image "pickable caméra" = détruite
                self.camera_deleted = False
        elif current_room == "pyimage4":
            # 575, 1000
            x_l_tol = screen_width / (1563 / 575)
            x_r_tol = screen_width / (192 / 125)
            # 565, 650
            y_l_tol = screen_height / (864 / 565)
            y_r_tol = screen_height / (432 / 325)
            if x_l_tol < self.rel_pos.get("x") < x_r_tol and y_l_tol < self.rel_pos.get("y") < y_r_tol:
                if not self.is_player_room_entered:
                    self.is_player_room_entered = True
                    # self.master.rect.create_dialog_box("player_room")
                self.master.rect.popup_draw.show_tip(self.rel_pos)
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.
                                 change_background("app_background",
                                                   self.master.desktop_closeup.get("desktop")))
            else:
                self.master.rect.popup_draw.hide_tip()
        elif current_room == "pyimage8":
            # 340, 1125
            x_l_tol = screen_width / (384 / 85)
            x_r_tol = screen_width / (512 / 375)
            # 380, 825
            y_l_tol = screen_height / (216 / 95)
            y_r_tol = screen_height / (288 / 275)
            if not self.is_drawing_book_discovered:
                self.is_drawing_book_discovered = True
                # self.master.rect.create_dialog_box("découverte_cahier_dessin")
            if x_l_tol < self.rel_pos.get("x") < x_r_tol and y_l_tol < self.rel_pos.get("y") < y_r_tol:
                self.master.rect.draw.show_tip(self.rel_pos)
                self.master.bind("<e>",
                                 lambda x: self.master.rect.
                                 change_background("app_background",
                                                   self.master.desktop_closeup.get("draw")))
            else:
                self.master.rect.draw.hide_tip()
        elif current_room == "pyimage9":
            # self.master.dots.check_collision(self.rel_pos)
            self.master.rect.changing_state_canvas_item(self.master.rect.camera, "hidden")
            if not self.are_drawings_discovered:
                self.are_drawings_discovered = True
                # self.master.rect.create_dialog_box("dessins", "black")
            if not self.are_dots_drawn and not self.has_monster_appeared:
                self.master.dots.start_game(self.img_list[self.index_dot])
                self.master.rect.canvas.bind("<Button-1>",
                                             lambda x: self.master.dots.get_x_y(self.rel_pos))
                self.master.rect.canvas.bind("<B1-Motion>",
                                             lambda x: self.master.dots.paint(self.rel_pos))
                self.master.rect.canvas.bind("<ButtonRelease-1>", lambda x:
                pen_channel.pause())
                self.are_dots_drawn = True
        elif current_room == "pyimage5":
            # 800, 1000
            x_l_tol = screen_width / (48 / 25)
            x_r_tol = screen_width / (192 / 125)
            # 50, 250
            y_l_tol = screen_height / (432 / 25)
            y_r_tol = screen_height / (432 / 125)
            if x_l_tol < self.rel_pos.get("x") < x_r_tol \
                    and y_l_tol < self.rel_pos.get("y") < y_r_tol:
                # print("Livres ???!!!")
                self.master.rect.see_books.show_tip(self.rel_pos)
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.
                                 change_background("app_background",
                                                   self.master.library_closeup.get("see_books")))
            else:
                self.master.rect.see_books.hide_tip()
        # regarde livres dispo
        elif current_room == "pyimage10":
            # print("Accès à tous les livres...")
            # 380, 480
            x_l_tol = screen_width / (384 / 95)
            x_r_tol = screen_width / (16 / 5)
            if x_l_tol < self.rel_pos.get("x") < x_r_tol:
                # print("LIVRE A LIRE")
                self.master.rect.open_family_book.show_tip(self.rel_pos)
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.
                                 change_background("app_background",
                                                   self.master.library_closeup.get("family_book")))
            else:
                self.master.rect.open_family_book.hide_tip()
        # joueur lit livre "famille"
        elif current_room == "pyimage11":
            # print(self.is_fam_book_read)
            if not self.is_fam_book_read:
                # print(txt_files_story("./dialog/dialog_text/lire_livre.txt"))
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
        # print(current_bg)
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

    def incr_door_try(self, event=None):
        self.door_try = self.door_try + 1
        return

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
        # print(self.prev_and_current_room)
        # porte principale --> cuisine OU bureau
        if prev_room == "pyimage3" and current_room in {"pyimage2", "pyimage4"}:
            self.master.rect.door_handle.hide_tip()
            self.master.unbind("<Button-1>")
        # cuisine --> toilette OU porte principale
        elif prev_room in {"pyimage25", "pyimage26"} and current_room in {"pyimage1", "pyimage3"}:
            # print("2")
            self.master.rect.orange_kitchen.hide_tip()
            self.master.rect.drawer_open.hide_tip()
        # cuisine --> oranges
        elif prev_room in {"pyimage25", "pyimage26"} and current_room == "pyimage6":
            # print("4 condition")
            self.master.rect.orange_kitchen.hide_tip()
        # cuisine --> brochure
        elif prev_room in {"pyimage25", "pyimage26"} and current_room == "pyimage7":
            # print("3 condition")
            self.master.rect.drawer_open.hide_tip()
        # orange --> cuisine (=/close-up)
        elif prev_room == "pyimage6" and current_room in {"pyimage25", "pyimage26"}:
            self.master.rect.orange_kitchen.hide_tip()
        # brochure --> toilette OU porte principale OU CUISINE
        elif prev_room == "pyimage7" and current_room in {"pyimage1", "pyimage3", "pyimage25", "pyimage26"}:
            # print("5 condition")
            self.master.rect.read_pamphlet_drawer.hide_tip()
            self.is_pamphlet_kitchen_read = False
            reset_story_reader(self.master)
            self.master.unbind("<e>")
        # bureau --> porte principale OU bibliothèque OU cahier dessin
        elif prev_room == "pyimage4" and current_room in {"pyimage3", "pyimage5", "pyimage8"}:
            # print("6 condition")
            self.master.rect.popup_draw.hide_tip()
        # cahier dessin --> porte principale OU bibliothèque OU dessiner OU bureau
        elif prev_room == "pyimage8" and current_room in {"pyimage3", "pyimage5", "pyimage9", "pyimage4"}:
            self.master.rect.draw.hide_tip()
            self.master.unbind("<e>")
        # dessiner --> porte principale OU bibliothèque OU bureau
        elif prev_room == "pyimage9" and current_room in {"pyimage3", "pyimage5", "pyimage4"}:
            self.master.rect.canvas.unbind("<Button-1>")
            self.master.rect.canvas.unbind("<B1-Motion>")
            self.master.rect.canvas.unbind("<ButtonRelease-1>")
            if self.is_camera_available and \
                self.master.rect.canvas.itemcget(self.master.rect.camera, "state") == "hidden":
                self.master.rect.changing_state_canvas_item(self.master.rect.camera, "normal")
            pen_channel.stop()
            # pygame.mixer.music.unload()
            self.master.dots.reset()
            self.master.dots.has_music_started = False
            self.are_dots_drawn = False
        # bibliothèque --> bureau OU close-up livres dispo
        elif prev_room == "pyimage5" and current_room in {"pyimage4", "pyimage10"}:
            self.master.rect.see_books.hide_tip()
        # close-up livres dispo --> bureau OU lire livre famille OU bibliothèque
        elif prev_room == "pyimage10" and current_room in {"pyimage4", "pyimage11", "pyimage5"}:
            self.master.rect.open_family_book.hide_tip()
        # lire livre famille --> bureau OU bibliothèque
        elif prev_room == "pyimage11" and current_room in {"pyimage4", "pyimage5"}:
            self.master.rect.open_family_book.hide_tip()
            self.is_fam_book_read = False
            reset_story_reader(self.master)
