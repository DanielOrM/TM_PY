class GameEventHandler:
    def __init__(self, master):
        self.master = master
        self.intro_initialized= False
        self.intro_ended = False

    def events_to_check(self):
        if not self.intro_initialized and not self.intro_ended:
            # DialogBoxes().dialog_to_use("intro")
            print("INTRO COMMENCE")
            self.master.rect.change_background("app_background", self.master.black_background)
            # self.master.rect.canvas.itemconfigure(self.master.rect.camera, state="hidden")
            self.master.rect.create_dialog_box("intro")
            # print("EN ATTENTE")
            self.intro_initialized = True
        elif self.intro_initialized and not self.intro_ended:
            # self.master.view.change_room("room_0")
            self.intro_ended = True
        else:
            print("Rien à signaler...")