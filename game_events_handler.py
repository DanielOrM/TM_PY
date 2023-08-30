"""Classe gérant tous les intéractions + event du jeu"""


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
        self.is_desktop_visible = False

    def events_to_check(self):
        """
        Images:
            - pyimage 1 = toilettes
            - pyimage 2 = cuisine
            - pyimage 3 = salle principale (porte)
            - pyimage 4 = chambre dessin
            - pyimage 5 = bibliothèque
        """
        if not self.intro_initialized and not self.intro_ended:
            # DialogBoxes().dialog_to_use("intro")
            print("INTRO COMMENCE")
            # windll.user32.BlockInput(True)
            # enlève souris input, click et intéractions avec clavier
            self.master.rect.change_background("app_background", self.master.black_background)
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
        elif self.get_current_room_img() == "pyimage3":
            # print("Là... ça marche. C'est la pièce principale.")
            self.master.rect.changing_state_canvas_item("camera_click", "normal")
            if self.camera_deleted:
                print("SALUT C'EST MOI LA CAMERA")
                self.master.rect.create_dialog_box("camera_trouvee")
                # évite de retoggle cette partie du code. iImage "pickable caméra" = détruite
                self.camera_deleted = False
        elif self.get_current_room_img() == "pyimage4":
            if 575 < self.rel_pos.get("x") < 1000 and 565 < self.rel_pos.get("y") < 650:
                print("DESSIN")
                print(f"x: {self.rel_pos.get('x')}, y: {self.rel_pos.get('y')}")
                self.master.rect.popup_draw.show_tip(self.rel_pos)
                # print(pygame.mouse.get_pressed())
                # print(pygame.mouse.get_pressed()[0])
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.change_background("app_background",
                                           self.master.desktop_closeup.get("desktop")))
            else:
                self.master.rect.popup_draw.hide_tip()
        elif self.get_current_room_img() == "pyimage5":
            if 800 < self.rel_pos.get("x") < 1000 and 50 < self.rel_pos.get("y") < 250:
                print("Livres ???!!!")
                self.master.rect.see_books.show_tip(self.rel_pos)
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.change_background("app_background",
                                           self.master.library_closeup.get("see_books")))
            else:
                self.master.rect.see_books.hide_tip()
        # regarde livres dispo
        elif self.get_current_room_img() == "pyimage7":
            print("Accès à tous les livres...")
            if 380 < self.rel_pos.get("x") < 480:
                print("LIVRE A LIRE")
                self.master.rect.open_family_book.show_tip(self.rel_pos)
                self.master.bind("<Button-1>",
                                 lambda x: self.master.rect.change_background("app_background",
                                           self.master.library_closeup.get("family_book")))
            else:
                self.master.rect.open_family_book.hide_tip()
        # joueur lit livre "famille"
        elif self.get_current_room_img() == "pyimage8":
            # print(self.rel_pos)
            self.master.rect.read_fam_book.show_tip(self.rel_pos)
            # quand joueur appuie sur E, ouvre image "read_fam_book" et enlève le texte affiché
            # self.master.bind("<E>", lambda x: self.master.rect.change_background("app_background", self.master.library_closeup.get("read_fam_book")), self.master.rect.read_fam_book.hide_tip())
            # self.master.bind("<e>", lambda x: self.master.rect.change_background("app_background", self.master.library_closeup.get("read_fam_book")))
            self.master.bind("<e>", lambda x: self.master.rect.change_background("app_background", self.master.library_closeup.get("read_fam_book")))
        if not self.get_current_room_img() == "pyimage3" and not self.camera_deleted:
            self.master.rect.changing_state_canvas_item("camera_click", "hidden")
        else:
            print("Rien à signaler...")

    def get_current_room_img(self):
        """
        Return n° pyimage actuelle (image fond d'écran)
        """
        # bg = self.master.rect.get_bg_att()
        # print(bg)
        return self.master.rect.get_key_val_canvas_obj("app_background", "image") # background
