# from ctypes import *


class GameEventHandler:
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

    def events_to_check(self):
        """
        Images:
            - pyimage 1 = toilettes
            - pyimage 2 = cuisine
            - pyimage 3 = salle principale (porte)
            - pyimage 4 = chambre dessin
            - pyimage 5 = bibliothèque
        """
        # print(self.x, self.y)
        # évite d'interrompre l'intro ou accidentellement trigger des conditions de la func "events_to_check"
        # if self.master.HS.winfo_ismapped():
        #     print("Encore à l'écran d'accueil!")
        #     return
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
                self.camera_deleted = False # évite de retoggle cette partie du code. L'image de la "pickable caméra" est bien détruite
        elif self.get_current_room_img() == "pyimage4":
            if 575 < self.rel_pos.get("x") < 1000 and 565 < self.rel_pos.get("y") < 650:
                print("DESSIN")
                print(f"x: {self.rel_pos.get('x')}, y: {self.rel_pos.get('y')}")
                self.master.rect.popup_draw.show_tip(self.rel_pos)
            else:
                self.master.rect.popup_draw.hide_tip()
        if not self.get_current_room_img() == "pyimage3" and not self.camera_deleted:
            self.master.rect.changing_state_canvas_item("camera_click", "hidden")
        else:
            print("Rien à signaler...")

    def get_current_room_img(self):
        # check si appareil photo est dans la pièce principale. Sinon, l'object "pickable" se déplace avec le joueur
        # bg = self.master.rect.get_bg_att()
        # print(bg)
        return self.master.rect.get_key_val_canvas_obj("app_background", "image") # background

