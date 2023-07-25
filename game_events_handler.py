class GameEventHandler:
    def __init__(self, master):
        self.master = master
        self.intro_initialized= False
        self.intro_ended = False
        self.camera_deleted = False
        self.are_rooms_visible = False

    def events_to_check(self):
        print(self.camera_deleted)
        if not self.intro_initialized and not self.intro_ended:
            # DialogBoxes().dialog_to_use("intro")
            # print("INTRO COMMENCE")
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
        elif self.camera_deleted:
            print("SALUT C'EST MOI LA CAMERA")
            self.master.rect.create_dialog_box("camera_trouvee")
            self.camera_deleted = False
        else:
            print("Rien à signaler...")


