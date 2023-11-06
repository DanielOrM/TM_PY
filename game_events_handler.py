"""Classe gérant tous les intéractions + event du jeu"""
import tkinter as tk
import pygame
from global_var import screen_height, screen_width
from images import bg_image_setup
from son.channels import pen_channel, music, monster_music
from son.random_sound_effects import play_sound_effect, SetInterval
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
        # self.img_list = ["./images/connect the dots/FishDrawnDotsSize.png"]
        # infrared
        self.are_infrared_lenses_seen = False
        self.are_drugs_seen = False

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
        self.master.game_controls.initialize_controls()
        self.master.rect.changing_state_canvas_item("camera_click", "normal")
        self.master.bind("<Motion>", self.master.motion)
        bg_music_path = "./son/musiques/MusiqueFond.mp3"
        bg_music = pygame.mixer.Sound(bg_music_path)
        music.play(bg_music, loops=-1)
        music.set_volume(0.8)

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
        # print(current_room)
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
            # activer musique de fond
            bg_music_path = "./son/musiques/MusiqueFond.mp3"
            bg_music = pygame.mixer.Sound(bg_music_path)
            music.play(bg_music, loops=-1)
            music.set_volume(0.8)
        elif current_room == "salle de bain":
            # close-up pour miroir + médocs
            if self.master.screen_width * 0.6 < self.rel_pos.get("x") < self.master.screen_width * (4 / 5) and \
                    0 < self.rel_pos.get("y") < self.master.screen_height / 3:
                self.master.rect.bathroom_mirror.show_tip(self.rel_pos)
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.
                                 change_background("app_background",
                                                   self.master.bathroom_closeup.get("mirror")))
            else:
                self.master.rect.bathroom_mirror.hide_tip()
        elif current_room == "mirroir":
            if self.master.screen_width / 7 * 4 < self.rel_pos.get("x") < self.master.screen_width / 7 * 5 and \
                    self.master.screen_height * 0.3 < self.rel_pos.get("y") < self.master.screen_height * 0.4:
                self.master.rect.bathroom_drugs.show_tip(self.rel_pos)
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.
                                 change_background("app_background",
                                                   self.master.bathroom_closeup.get("drugs")))
            else:
                self.master.rect.bathroom_drugs.hide_tip()
        elif current_room == "médicaments":
            # self.master.rect.canvas.create_rectangle(x_left, y_bot, x_right, y_top, fill="RED")
            if self.are_drugs_seen:
                x_left = self.master.screen_width * 0.5
                x_right = self.master.screen_width*0.7
                y_bot = self.master.screen_height * 0.8
                y_top = self.master.screen_height * 0.93
                if x_left < self.rel_pos.get("x") < x_right and y_bot < self.rel_pos.get("y") < y_top:
                    if not self.master.rect.drugs.available:
                        self.master.rect.get_drugs.show_tip(self.rel_pos)
                        drugs_available = self.master.bind("<Button-1>", lambda x: self.master.rect.
                                                           make_item_available(
                            self.master.rect.drugs, drugs_available))
                else:
                    self.master.rect.get_drugs.hide_tip()
        elif current_room == "cuisine normale":
            if screen_width / (1536 / 575) < self.rel_pos.get("x") < screen_width / (192 / 125) \
                    and 0 < self.rel_pos.get("y") < screen_height / (72 / 25):
                self.master.pages["room_1"] = \
                    bg_image_setup("./images/rooms/changed_rooms/kitchen/PA_CH_Cuisine.png", name="cuisine changée")
                self.master.view.simple_transition("room_1")
        elif current_room == "cuisine changée":
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
        elif current_room == "close-up oranges":
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
        elif current_room == "tiroir cuisine":
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
        elif current_room == "pièce porte":
            if not self.are_randm_sound_activated:
                self.are_randm_sound_activated = True
                # sons random chaque 5 minutes
                SetInterval(play_sound_effect, 300)
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
        elif current_room == "pièce dessin":
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
        elif current_room == "close-up bureau":
            # 340, 1125
            x_l_tol = screen_width / (384 / 85)
            x_r_tol = screen_width / (512 / 375)
            # 380, 825
            y_l_tol = screen_height / (216 / 95)
            y_r_tol = screen_height / (288 / 275)
            if not self.is_drawing_book_discovered:
                self.is_drawing_book_discovered = True
                # self.master.rect.create_dialog_box("découverte_cahier_dessin")
            if x_l_tol < self.rel_pos.get("x") < x_r_tol and y_l_tol < self.rel_pos.get("y") < y_r_tol and \
                    not self.has_monster_appeared:
                self.master.rect.draw.show_tip(self.rel_pos)
                self.master.bind("<e>",
                                 lambda x: self.master.rect.
                                 change_background("app_background",
                                                   self.master.desktop_closeup.get("draw")))
            else:
                self.master.rect.draw.hide_tip()
        elif current_room == "dessin":
            # self.master.dots.check_collision(self.rel_pos)
            self.master.rect.changing_state_canvas_item(self.master.rect.camera, "hidden")
            if not self.are_drawings_discovered:
                self.are_drawings_discovered = True
                self.master.rect.create_dialog_box("dessins", "black")
            if not self.are_dots_drawn:
                self.master.dots.start_game(self.img_list[self.index_dot])
                self.master.rect.canvas.bind("<Button-1>",
                                             lambda x: self.master.dots.get_x_y(self.rel_pos))
                self.master.rect.canvas.bind("<B1-Motion>",
                                             lambda x: self.master.dots.paint(self.rel_pos))
                self.master.rect.canvas.bind("<ButtonRelease-1>", lambda x:
                pen_channel.pause())
                self.are_dots_drawn = True
        elif current_room == "bibliothèque":
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
            if self.are_infrared_lenses_seen:
                y_error_margin = self.master.screen_height / (432 / 5)
                if self.master.screen_height / (216 / 145) - y_error_margin < self.rel_pos.get("y") < \
                        self.master.screen_height / (36 / 25) + y_error_margin and self.master.screen_width / (768 / 55) \
                        < self.rel_pos.get("x") < self.master.screen_width / (768 / 185):
                    if not self.master.rect.infrared_lenses.available:
                        self.master.rect.get_infrared_lenses.show_tip(self.rel_pos)
                        infrared_available = self.master.bind("<Button-1>", lambda x: self.master.rect.
                                                              make_item_available(
                            self.master.rect.infrared_lenses, infrared_available))
                else:
                    self.master.rect.get_infrared_lenses.hide_tip()
        # regarde livres dispo
        elif current_room == "livres":
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
                                                   self.master.library_closeup.get("read_fam_book")))
            else:
                self.master.rect.open_family_book.hide_tip()
        # joueur lit livre "famille"
        elif current_room == "lire famille livre":
            # print(self.is_fam_book_read)
            if not self.is_fam_book_read:
                # print(txt_files_story("./dialog/dialog_text/lire_livre.txt"))
                txt_story_reader(self.master, "./dialog/dialog_text/lire_livre.txt")
            self.is_fam_book_read = True
        if not current_room == "pièce porte" and not self.camera_deleted:
            self.master.rect.changing_state_canvas_item("camera_click", "hidden")
        else:
            pass

    def check_monster_taken_by_camera(self):
        """
        Func pour appari° monstre
        """
        if not self.has_monster_appeared:
            return
        else:
            if self.master.monster.is_monster_hunting:
                monster_pos = self.master.rect.canvas.bbox(self.master.monster.monster_design)  # x1, y1, x2, y2
                x_monster_range = monster_pos[0], monster_pos[2]
                y_monster_range = monster_pos[1], monster_pos[3]
                # check si photo prise DANS img monstre
                # print(f"x range: {x_monster_range}, start x: {self.check_start_x}, end x: {self.check_end_x}")
                # print(f"x range: {y_monster_range}, start x: {self.check_start_y}, end x: {self.check_end_y}")
                if x_monster_range[0] < self.check_start_x < self.check_end_x < x_monster_range[1] and \
                        y_monster_range[0] < self.check_start_y < self.check_end_y < y_monster_range[1]:
                    monster_music.stop()
                    # enlève monstre, joueur a réussi
                    self.master.monster.hide_monster()
                else:
                    print("Monstre PAS pris en photo")
            else:
                print("Bah.. le monstre chasse pas donc c'est bon")

    def check_for_infrared_lenses(self):
        """
        Si prend une photo dans endroit particulier bibliothèque (en bleu):
            - débloque un dialogue
            - possible de ramasser lentilles infrarouges
            - nouvelle touche <r> (sur zone de drag + drop)
        """
        current_room = self.get_current_room_img()
        if current_room != "bibliothèque":
            return
        # print(f"gauche{self.check_start_x}, droit{self.check_end_x}, bas:{self.check_start_y},
        # haut{self.check_end_y}")
        y_error_margin = self.master.screen_height / (432 / 5)
        if self.master.screen_height / (216 / 145) - y_error_margin < self.check_start_y < self.check_end_y < \
                self.master.screen_height / (36 / 25) + y_error_margin and self.master.screen_width / (768 / 55) \
                < self.check_start_x < self.check_end_x < self.master.screen_width / (768 / 185):
            self.master.rect.create_dialog_box("infrarouges_trouvee")
            self.are_infrared_lenses_seen = True

    def check_for_drugs(self):
        """
        Si prend une photo dans endroit tiroir, médocs:
            - débloque un dialogue
            - possible de ramasser médocs
            - nouvelle touche <f> (prendre médoc)
        """
        current_room = self.get_current_room_img()
        if current_room != "médicaments":
            return
        # print(f"gauche{self.check_start_x}, droit{self.check_end_x}, bas:{self.check_start_y},
        # haut{self.check_end_y}")
        x_left = self.master.screen_width / 7
        x_right = self.master.screen_width / 7 * 5
        y_bot = self.master.screen_height * 0.4
        y_top = self.master.screen_height * 0.95
        if y_bot < self.check_start_y < self.check_end_y < y_top and x_left < self.check_start_x < self.check_end_x < \
                x_right:
            self.master.rect.create_dialog_box("médocs")
            self.are_drugs_seen = True

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
        if prev_room == "pièce porte" and current_room in {"cuisine normale", "pièce dessin"}:
            self.master.rect.door_handle.hide_tip()
            self.master.unbind("<Button-1>")
        # cuisine --> toilette OU porte principale
        elif prev_room == "cuisine changée" and current_room in {"salle de bain", "pièce porte"}:
            # print("2")
            self.master.rect.orange_kitchen.hide_tip()
            self.master.rect.drawer_open.hide_tip()
        # cuisine --> oranges
        elif prev_room == "cuisine changée" and current_room == "close-up oranges":
            # print("4 condition")
            self.master.rect.orange_kitchen.hide_tip()
        # cuisine --> brochure
        elif prev_room == "cuisine changée" and current_room == "tiroir cuisine":
            # print("3 condition")
            self.master.rect.drawer_open.hide_tip()
        # orange --> cuisine (=/close-up)
        elif prev_room == "close-up oranges" and current_room == "cuisine changée":
            self.master.rect.orange_kitchen.hide_tip()
        # brochure --> toilette OU porte principale OU CUISINE
        elif prev_room == "tiroir cuisine" and current_room in {"salle de bain", "pièce porte", "cuisine changée"}:
            # print("5 condition")
            self.master.rect.read_pamphlet_drawer.hide_tip()
            self.is_pamphlet_kitchen_read = False
            reset_story_reader(self.master)
            self.master.unbind("<e>")
        # salle de bain --> close-up
        elif prev_room == "salle de bain" and current_room == "mirroir":
            self.master.rect.bathroom_mirror.hide_tip()
            self.master.unbind("<Button-1>")
        # mirroir --> salle de bain OU close-up médocs
        elif prev_room == "mirroir" and current_room in {"salle de bain", "médicaments"}:
            self.master.rect.bathroom_drugs.hide_tip()
            self.master.unbind("<Button-1>")
        # close-up médocs --> salle de bain OU cuisine
        elif prev_room == "médicaments" and current_room in {"salle de bain", "cuisine normale", "cuisine changée"}:
            pass
        # bureau --> porte principale OU bibliothèque OU close-up bureau
        elif prev_room == "pièce dessin" and current_room in {"pièce porte", "bibliothèque", "close-up bureau"}:
            # print("6 condition")
            self.master.rect.popup_draw.hide_tip()
        # cahier dessin --> porte principale OU bibliothèque OU dessiner OU bureau
        elif prev_room == "close-up bureau" and current_room in {"pièce porte",
                                                                 "bibliothèque", "dessin", "pièce dessin"}:
            self.master.rect.draw.hide_tip()
            self.master.unbind("<e>")
        # dessiner --> porte principale OU bibliothèque OU bureau
        elif prev_room == "dessin" and current_room in {"pièce porte", "bibliothèque", "pièce dessin",
                                                        "screamer écran noir", "screamer écran blanc"}:
            self.master.rect.canvas.unbind("<Button-1>")
            self.master.rect.canvas.unbind("<B1-Motion>")
            self.master.rect.canvas.unbind("<ButtonRelease-1>")
            if self.is_camera_available and \
                    self.master.rect.canvas.itemcget(self.master.rect.camera, "state") == "hidden" and \
                    current_room not in {"screamer écran noir", "screamer écran blanc"}:
                self.master.rect.changing_state_canvas_item(self.master.rect.camera, "normal")
            pen_channel.stop()
            # pygame.mixer.music.unload()
            self.master.dots.reset()
            self.master.dots.has_music_started = False
            self.are_dots_drawn = False
        # bibliothèque --> bureau OU close-up livres dispo
        elif prev_room == "bibliothèque" and current_room in {"pièce dessin", "livres"}:
            self.master.rect.see_books.hide_tip()
            if self.are_infrared_lenses_seen:
                self.master.unbind("<Button-1>")
                self.master.rect.get_infrared_lenses.hide_tip()
        # close-up livres dispo --> bureau OU lire livre famille OU bibliothèque
        elif prev_room == "livres" and current_room in {"pièce dessin", "lire famille livre", "bibliothèque"}:
            self.master.rect.open_family_book.hide_tip()
        # lire livre famille --> bureau OU bibliothèque
        elif prev_room == "lire famille livre" and current_room in {"pièce dessin", "bibliothèque"}:
            self.master.rect.open_family_book.hide_tip()
            self.is_fam_book_read = False
            reset_story_reader(self.master)
