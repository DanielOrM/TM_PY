"""Module utilisé pour faire fonctionner la plus grandie partie de mon jeu."""
import tkinter as tk
from tkinter import VERTICAL, HORIZONTAL, PhotoImage
import sys
import os
import pygame
import threading
from txt_story_reader import txt_files_story
from threading import Thread
from PIL import Image, ImageTk
from images import bg_image_setup, open_image_setup_file
from fade_transition import FadeTransition, FadeIn
from dialog.dialog_boxes import DialogBoxes
from game_events_handler import GameEventHandler
from hover_message import create_hover_message, HoverMessage, HoverMessRelPos
from global_var import screen_width, screen_height
from connect_dots import ConnectDotsGame
from fonts import RenderFont
from son.channels import music, monster_music
from random import randrange


global restart
restart = False

class HomeScreen:
    """
    Écran d'accueil
        - image d'accueil à changer
        - bouton jouer/quitter (à replacer)
        - musique de fond
    """
    def __init__(self, master):
        self.master = master
        # configure de grid pour le reste du code
        self.master.grid_rowconfigure(0, weight=1)  # pour row 0
        self.master.grid_columnconfigure(0, weight=1)  # pour column 0
        # écran d'accueil initial
        self.hs_image = bg_image_setup("./images/homescreen/PA_PX_BackgroundRework.png", name="écran d'accueil")
        self.hs_tuto = bg_image_setup("./images/homescreen/GradientBlue.png", name="tuto bg")    # tuto img
        self.hs_canvas_img = None
        self.hs_canvas = tk.Canvas(master, height=screen_height, width=screen_width)
        self.apply_hs_canvas_image()
        # commencer le jeu
        self.start_button = self.hs_canvas.create_text(
            (screen_width/5*4, screen_height/3*2+40),
            text="Jouer", fill="white", font=("Helvetica", 30, "italic"))
        # regarder touches, donc mouvements, actions, etc.
        self.tuto = self.hs_canvas.create_text(
            (screen_width/5*4,  screen_height/3*2+100),
            text="Tutoriel", fill="white", font=("Helvetica", 30, "italic"))
        """
        Tuto icon
            - recommended size: 147x95
        """
        self.camera = self.master.camera
        self.camera_icon = None
        self.camera_tuto_txt = None
        self.album_ref = self.master.album
        self.album = self.resizeImage(self.album_ref, 147, 95)
        self.album_icon = None
        self.album_tuto_txt = None
        self.motion_img = open_image_setup_file("./images/homescreen/icons/PA_NB_MotionIcon.png")
        self.motion_icon = None
        self.motion_tuto_txt = None
        self.pencil_img = open_image_setup_file("./images/homescreen/icons/PA_NB_Pencil.png")
        self.pencil_icon = None
        self.pencil_tuto_txt = None
        self.red_button_img = open_image_setup_file("./images/homescreen/icons/PA_NB_RedButton.png")
        self.red_button_icon = None
        self.red_button_tuto_txt = None
        self.unzoom_img = open_image_setup_file("./images/homescreen/icons/PA_NB_Unzoom.png")
        self.unzoom_icon = None
        self.unzoom_tuto_txt = None

        # quitter tuto
        self.exit_tuto = None
        # quitter le jeu
        self.exit_game_button = self.hs_canvas.create_text(
            (screen_width / 5 * 4, screen_height / 3 * 2 + 160),
            text="Quitter le jeu", fill="white", font=("Helvetica", 30, "italic"))
        # commencer le jeu-bind
        self.hs_canvas.tag_bind(self.start_button, "<Button-1>", self.intro)
        self.hs_canvas.tag_bind(self.start_button, "<Enter>", lambda x: self.hover_text(self.start_button))
        self.hs_canvas.tag_bind(self.start_button, "<Leave>", lambda x: self.exit_text(self.start_button))
        # regarder tuto-bind
        self.hs_canvas.tag_bind(self.tuto, "<Button-1>", self.show_tuto)
        self.hs_canvas.tag_bind(self.tuto, "<Enter>", lambda x: self.hover_text(self.tuto))
        self.hs_canvas.tag_bind(self.tuto, "<Leave>", lambda x: self.exit_text(self.tuto))
        # quitter jeu-bind
        self.hs_canvas.tag_bind(self.exit_game_button, "<Button-1>", self.exit_game)
        self.hs_canvas.tag_bind(self.exit_game_button, "<Enter>", lambda x: self.hover_text(self.exit_game_button))
        self.hs_canvas.tag_bind(self.exit_game_button, "<Leave>", lambda x: self.exit_text(self.exit_game_button))
        self.hs_canvas.grid_propagate(False)
        self.hs_canvas.grid()
        music_path = "son/musiques/HomeScreenLoopMusic.mp3"
        homescreen_music = pygame.mixer.Sound(music_path)
        music.play(homescreen_music, loops=-1)
        self.master.mainloop()  # A NE PAS CHANGER --> risque d'erreurs

    def resizeImage(self, img, newWidth, newHeight):
        """
        Redimensionne image
        """
        oldWidth = img.width()
        oldHeight = img.height()
        newPhotoImage = PhotoImage(width=newWidth, height=newHeight)
        for x in range(newWidth):
            for y in range(newHeight):
                xOld = int(x * oldWidth / newWidth)
                yOld = int(y * oldHeight / newHeight)
                rgb = '#%02x%02x%02x' % img.get(xOld, yOld)
                newPhotoImage.put(rgb, (x, y))
        return newPhotoImage

    def hover_text(self, tag_or_id):
        self.hs_canvas.itemconfigure(tag_or_id, fill="gray")

    def exit_text(self, tag_or_id):
        self.hs_canvas.itemconfigure(tag_or_id, fill="white")

    def exit_game(self, event=None):
        self.master.destroy()
        sys.exit()

    def exit_tuto_button(self, event=None):
        """
        Crée bouton pour quitter tuto
        """
        self.exit_tuto = self.hs_canvas.create_text(
            (screen_width / 5 * 4, screen_height / 3 * 2 + 200),
            text="Quitter le tutoriel", fill="white", font=("Helvetica", 26, "italic"))
        self.hs_canvas.tag_bind(self.exit_tuto, "<Button-1>", self.hide_tuto)
        self.hs_canvas.tag_bind(self.exit_tuto, "<Enter>", lambda x: self.hover_text(self.exit_tuto))
        self.hs_canvas.tag_bind(self.exit_tuto, "<Leave>", lambda x: self.exit_text(self.exit_tuto))

    def apply_hs_canvas_image(self):
        """
        Application image écran accueil
            - taille
            - position
            - titre
        """
        title_height = self.master.winfo_screenheight()/4
        title_width = self.master.winfo_screenwidth()/2
        center_height = self.master.winfo_screenheight()/2
        center_width = self.master.winfo_screenwidth()/2
        self.master.home_s = self.hs_canvas
        self.hs_canvas_img = self.hs_canvas.create_image(center_width, center_height, image=self.hs_image)

    def intro(self, event=None):
        """
        Lancement intro réveil
        """
        music.stop()
        self.hs_canvas.grid_remove()
        self.check_game_e()

    def show_hs_buttons(self, event=None):
        """
        Montre écran avec:
            - jouer
            - tutoriel
            - quitter le jeu
        Enlève:
            - quitter tuto
        """
        self.hs_canvas.itemconfig(self.start_button, state="normal")
        self.hs_canvas.itemconfig(self.tuto, state="normal")
        self.hs_canvas.itemconfig(self.exit_game_button, state="normal")
        self.hs_canvas.itemconfig(self.exit_tuto, state="hidden")

    def hide_hs_buttons(self, event=None):
        """
        Cache écran avec:
            - jouer
            - tutoriel
            - quitter le jeu
        """
        self.hs_canvas.itemconfig(self.start_button, state="hidden")
        self.hs_canvas.itemconfig(self.tuto, state="hidden")
        self.hs_canvas.itemconfig(self.exit_game_button, state="hidden")
        if self.exit_tuto:
            self.hs_canvas.itemconfig(self.exit_tuto, state="normal")

    def create_all_tuto_icons_txt(self):
        """
        Initialise les icônes
        """
        screen_w_space = self.master.screen_width / 3
        screen_w_img_text = screen_w_space / 3
        screen_w_img_pos = self.master.screen_width / 12 * 5 / 3
        screen_h_space = self.master.screen_height / 6 * (3 / 2)
        screen_h_img_text = screen_h_space / 8
        screen_h_img_pos = self.master.screen_width / 4
        # création icônes + textes
        # camera + texte
        self.camera_icon = self.hs_canvas.create_image((screen_w_img_pos, screen_h_space), image=self.camera)
        self.camera_tuto_txt = self.hs_canvas.create_text(
            (screen_w_img_pos * 3 / 2 + screen_w_img_text, screen_h_space + screen_h_img_text),
            text=txt_files_story("./tuto texts/camera_tuto.txt"),
            fill="white", font=("Helvetica", 15, "italic"))
        # album photo + texte
        self.album_icon = self.hs_canvas.create_image((screen_w_img_pos * 4, screen_h_space), image=self.album)
        self.album_tuto_txt = self.hs_canvas.create_text(((screen_w_img_pos * 3 / 2) * 3 + screen_w_img_text,
                                                          screen_h_space),
                                                         text=txt_files_story("./tuto texts/album_tuto.txt"),
                                                         fill="white", font=("Helvetica", 15, "italic"))
        # mouvement + texte
        self.motion_icon = self.hs_canvas.create_image((screen_w_img_pos, screen_h_img_pos*11/10), image=self.motion_img)
        self.motion_tuto_txt = self.hs_canvas.create_text((screen_w_img_pos * 3 / 2 + screen_w_img_text,
                                                          screen_h_img_pos*11/10),
                                                         text=txt_files_story("./tuto texts/motion_tuto.txt"),
                                                         fill="white", font=("Helvetica", 15, "italic"))
        # quitter le jeu + texte
        self.red_button_icon = self.hs_canvas.create_image((screen_w_img_pos * 4,
                                                          screen_h_img_pos*11/10), image=self.red_button_img)
        self.red_button_tuto_txt = self.hs_canvas.create_text(((screen_w_img_pos * 3 / 2) * 3 + screen_w_img_text/3*2,
                                                          screen_h_img_pos*11/10),
                                                          text=txt_files_story("./tuto texts/exit_game_tuto.txt"),
                                                          fill="white", font=("Helvetica", 15, "italic"))
        # dessiner + texte
        self.pencil_icon = self.hs_canvas.create_image((screen_w_img_pos, screen_h_space+screen_h_img_pos),
                                                       image=self.pencil_img)
        self.pencil_tuto_txt = self.hs_canvas.create_text((screen_w_img_pos*3/2 + screen_w_img_text*6/5,
                                                           screen_h_space+screen_h_img_pos),
                                                          text=txt_files_story("./tuto texts/draw_tuto.txt"),
                                                          fill="white", font=("Helvetica", 15, "italic"))
        # quitter close-up + texte
        self.unzoom_icon = self.hs_canvas.create_image((screen_w_img_pos*4, screen_h_space+screen_h_img_pos),
                                                       image=self.unzoom_img)
        self.unzoom_tuto_txt = self.hs_canvas.create_text(((screen_w_img_pos * 3 / 2) * 3 + screen_w_img_text,
                                                           screen_h_space+screen_h_img_pos),
                                                          text=txt_files_story("./tuto texts/exit_close_up_tuto.txt"),
                                                          fill="white", font=("Helvetica", 15, "italic"))

    def show_all_tuto_icons_txt(self):
        """
        Montre tous les icônes + textes dans tuto
            - évite de les récréer
        """
        self.hs_canvas.itemconfigure(self.camera_icon, state="normal")
        self.hs_canvas.itemconfigure(self.camera_tuto_txt, state="normal")
        self.hs_canvas.itemconfigure(self.album_icon, state="normal")
        self.hs_canvas.itemconfigure(self.album_tuto_txt, state="normal")
        self.hs_canvas.itemconfigure(self.motion_icon, state="normal")
        self.hs_canvas.itemconfigure(self.motion_tuto_txt, state="normal")
        self.hs_canvas.itemconfigure(self.red_button_icon, state="normal")
        self.hs_canvas.itemconfigure(self.red_button_tuto_txt, state="normal")
        self.hs_canvas.itemconfigure(self.pencil_icon, state="normal")
        self.hs_canvas.itemconfigure(self.pencil_tuto_txt, state="normal")
        self.hs_canvas.itemconfigure(self.unzoom_icon, state="normal")
        self.hs_canvas.itemconfigure(self.unzoom_tuto_txt, state="normal")

    def hide_all_icons(self, event=None):
        """
        Cache tous les icônes + textes dans le tuto
        """
        self.hs_canvas.itemconfigure(self.camera_icon, state="hidden")
        self.hs_canvas.itemconfigure(self.camera_tuto_txt, state="hidden")
        self.hs_canvas.itemconfigure(self.album_icon, state="hidden")
        self.hs_canvas.itemconfigure(self.album_tuto_txt, state="hidden")
        self.hs_canvas.itemconfigure(self.motion_icon, state="hidden")
        self.hs_canvas.itemconfigure(self.motion_tuto_txt, state="hidden")
        self.hs_canvas.itemconfigure(self.red_button_icon, state="hidden")
        self.hs_canvas.itemconfigure(self.red_button_tuto_txt, state="hidden")
        self.hs_canvas.itemconfigure(self.pencil_icon, state="hidden")
        self.hs_canvas.itemconfigure(self.pencil_tuto_txt, state="hidden")
        self.hs_canvas.itemconfigure(self.unzoom_icon, state="hidden")
        self.hs_canvas.itemconfigure(self.unzoom_tuto_txt, state="hidden")

    def show_tuto(self, event=None):
        """
        Crée une image contenant plusieurs canvas item avec textes
            - caméra
                - drag + drop
            - ouvrir album photo
                - middle click
            - mouvement
                - a, d
            - quitter le jeu
                - q
            - dessiner
                - click gauche
            - quitter un close-up
                - s
        """
        self.hs_canvas.itemconfigure(self.hs_canvas_img, image="tuto bg")
        self.hide_hs_buttons()
        if not self.exit_tuto:
            self.exit_tuto_button()
        if not self.camera_icon:    # juste besoin de check pour le 1er (suffisant)
            self.create_all_tuto_icons_txt()
        else:
            self.show_all_tuto_icons_txt()

    def hide_tuto(self, event=None):
        """
        Cache img tuto
            - change img state de
        """
        self.hide_all_icons()
        self.show_hs_buttons()
        self.hs_canvas.itemconfigure(self.hs_canvas_img, image="écran d'accueil")

    def check_game_e(self, event=None):
        """
        Raccourci pour func check_game_events
        """
        self.master.check_game_events()


class App(tk.Tk):
    """
    Application:
        - room_2 = salle de bain
            - bureau (close up)
        - room_1 = cuisine
        - room_0 = pièce principale
        - room1 = chambre dessin
        - room2 = bibliothèque
    """
    def __init__(self):
        super().__init__()
        self.title("Mon nom est...")
        # fonts
        self.fonts_list = []
        self.index = 2
        self.death_screen = bg_image_setup("./images/death screen/PA_DeathScreenFinal.png", name="death screen")
        self.pages_name = ["room_2", "room_1", "room_0", "room1", "room2"]
        self.pages_file_location = {
            "room_2": "./images/rooms/real_rooms/bathroom/PA_SalleDeBain.png",
            "room_1": "./images/rooms/real_rooms/kitchen/PA_Cuisine.png",
            "room_0": "./images/rooms/real_rooms/main_door/PA_PorteFermée.png",
            "room1": "./images/rooms/real_rooms/player_room/PA_CarnetDessinBureau.png",
            "room2": "./images/rooms/real_rooms/library/PA_Bibliothèque.png"
        }
        self.pages = {
            "room_2": bg_image_setup(self.pages_file_location.get("room_2"), name="salle de bain"),
            "room_1": bg_image_setup(self.pages_file_location.get("room_1"), name="cuisine normale"),
            "room_0": bg_image_setup(self.pages_file_location.get("room_0"), name="pièce porte"),
            "room1": bg_image_setup(self.pages_file_location.get("room1"), name="pièce dessin"),
            "room2": bg_image_setup(self.pages_file_location.get("room2"), name="bibliothèque")
        }
        # cuisine
        self.kitchen_closeup = {
            "oranges":
                bg_image_setup("./images/rooms/changed_rooms/kitchen/PA_CH_CuisineDésordreZoom.png",
                               name="close-up oranges"),
            "drawer":
                bg_image_setup("./images/rooms/changed_rooms/kitchen/PA_CH_CuisineTiroir.png", name="tiroir cuisine")
        }
        # chambre dessin
        self.desktop_closeup = {
            "desktop":
                bg_image_setup("./images/rooms/real_rooms/player_room/PA_CarnetDessinZoom.png", name="close-up bureau"),
            "draw":
                bg_image_setup("./images/rooms/real_rooms/player_room/PA_PapierDessin.png", name="dessin"),
        }
        # bibliothèque
        self.library_closeup = {
            "see_books": bg_image_setup("./images/rooms/real_rooms/library/PA_LivreZoom.png",
                                        name="livres"),
            "read_fam_book": bg_image_setup("./images/rooms/real_rooms/library/PA_LivreTrouvé.png",
                                            name="lire famille livre")
        }
        self.camera = open_image_setup_file("./images/player/PA_NB_PhotoCameraFromBehind.png")\
            .subsample(2,2) # image caméra 2 fois plus petite
        self.album = open_image_setup_file("./images/player/PA_NB_Album.png")
        self.left_arrow = open_image_setup_file("./images/player/red_arrow_left.png")\
            .subsample(16, 16)
        self.right_arrow = open_image_setup_file("./images/player/red_arrow_right.png")\
            .subsample(16, 16)
        self.black_background = bg_image_setup("images/intro/NB_BlackBox.png", name="écran noir intro")
        # dimensions écran
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.width = int(self.screen_width / 2)
        self.height = int(self.screen_height / 2)
        # position x et y centre écran
        self.center_x = int((self.screen_width / 4))
        self.center_y = int((self.screen_height / 4))
        # application dimensions initiales à fenêtre + centre fenêtre
        self.geometry(f"{self.width}x{self.height}+{self.center_x}+{self.center_y}")
        # widgets
        self.view = View(self)
        self.full_w = FullScreenWindow(self)
        self.game_controls = Control(self)
        self.rect = CanvasHandler(self) # rectangle photo dimensions
        self.fade = FadeTransition(self)
        self.dial = DialogBoxes(self)
        # self.HS = HomeScreen(self)

        # handler d'évents avec classe GameEventHandler
        self.game_e_handler = GameEventHandler(self)

        # connect the dots
        self.dots = ConnectDotsGame(self)
        self.fade_in = FadeIn(self)

        # HS canvas
        self.home_s = None

        # monstre widget
        self.monster = Monster(self)

    def check_game_events(self, event=None):
        """
        Raccourci pour func events_to_check
        """
        self.game_e_handler.events_to_check()

    def motion(self, event):
        """
        Déplacement souris
            - obtient x,y coords souris + les remplace dans game_e_handler
            - appelle func check_game_events
        """
        self.game_e_handler.rel_pos["x"], self.game_e_handler.rel_pos["y"] = event.x, event.y
        # print(self.game_e_handler.rel_pos["x"], self.game_e_handler.rel_pos["y"])
        self.check_game_events()


class View(tk.Frame):
    """
    Classe gérant quelques aspects visuels de la fenêtre principale (App)
    """
    def __init__(self, master):
        super().__init__(master)

    def change_room(self, room_name):
        """
        Change image pièce après transition
        - avec son
        """
        self.master.fade.create_transition(True)
        self.master.rect.change_background("app_background",
                                            self.master.pages.get(f"{room_name}"))

    def simple_transition(self, room_name):
        """
        Change image pièce après transition
        - pas de son
        """
        self.master.fade.create_transition()
        self.master.rect.change_background("app_background",
                                           self.master.pages.get(f"{room_name}"))

    def show_album(self, event=None):
        """
        Ouvre le
        """
        self.master.rect.open_album()


class Control:
    """
    Événements gérés:
        - a: déplacement pièce à gauche
        - d: déplacement pièce à droite
        - middle-click: ouvre/ferme album photo
    """

    def __init__(self, master):
        self.master = master

    def initialize_controls(self):
        self.master.bind("<a>", self.change_room_left)  # aller à gauche
        self.master.bind("<d>", self.change_room_right)  # aller à droite
        self.master.bind("<s>", self.remove_closeup) # enlève close-up
        self.master.bind("<Button-2>", self.see_album)  # button 2 => mid click
        self.master.bind("<q>", self.exit_game)  # quitte programme

    def exit_game(self, event=None):
        """
        Mieux d'utiliser exit_game de class HomeScreen
            - problème: ne termine pas complètement python (arrière-plan)
        """
        os._exit(0)

    def change_room_left(self, event=None):
        """
        Func appellée après <a>
            - index diminue de 1
        """
        if self.master.index > 0:
            self.master.index -= 1
            # print(self.master.index)
            self.master.view.change_room(self.master.pages_name[self.master.index])
        else:
            print("C'est un mur...")
        return "break"

    def change_room_right(self, event=None):
        """
        Func appellée après <d>
            - index augmente de 1
        """
        if self.master.index < 4:
            self.master.index += 1
            # print(self.master.index)
            self.master.view.change_room(self.master.pages_name[self.master.index])
        else:
            print("C'est un mur...")
        return "break"

    def remove_closeup(self, event=None):
        """
        Func appellée après <s>:
            - change background avec prev_room (list dans game_e_handler)
        """
        current_room = self.master.game_e_handler.get_current_room_img()
        if current_room in {"close-up oranges", "tiroir cuisine", "close-up bureau", "dessin",
                            "livres", "lire famille livre"}:
            self.master.rect.change_background("app_background",
                                               self.master.pages.get(self.master.pages_name[self.master.index]))

    def see_album(self, event=None):
        """
        Appelle func show_album
        """
        self.master.view.show_album()


class FullScreenWindow(tk.Frame):
    """
    Événements gérés:
    - plein écran <F11> ou <Fn> + <F11>
    - <Escape> pour quitter plein écran
    """

    def __init__(self, master):
        super().__init__(master)
        self.is_fullscreen = True
        self.initial_fullscreen()
        # self.pages
        master.bind("<F11>" or "<Fn> + <F11>", self.toggle_fullscreen)
        master.bind("<Escape>", self.exit_fullscreen)

    def initial_fullscreen(self, event=None):
        self.master.attributes("-fullscreen", self.is_fullscreen)

    def toggle_fullscreen(self, event=None):
        """
        Écran jeu = plein écran
        Check si écran déjà fullscreen.
        """
        if self.is_fullscreen == True:
            return
        else:
            self.is_fullscreen = not self.is_fullscreen  # toggle boolean
            self.master.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def exit_fullscreen(self, event=None):
        """
        <Esc>: quitte plein écran
        """
        if self.is_fullscreen == False:
            return
        else:
            self.is_fullscreen = not self.is_fullscreen  # toggle boolean self.is_fullscreen
            self.master.attributes("-fullscreen", self.is_fullscreen)
        return "break"


class CanvasHandler(tk.Frame):
    """
    CanvasHandler:
        - se charge de créer obj. "canevas"
        - change image fond d'écran
        - intéractions avec images
        - messages pop-up
        - Photos:
            - ouvre l'album photos
            - prend photos
            - liste photos
    """
    def __init__(self, master):
        super().__init__(master)
        self.x = self.y = 0
        self.canvas = tk.Canvas(self.master, cursor="cross",
                                height=self.master.winfo_screenheight(),
                                width=self.master.winfo_screenwidth(),
                                )
        self.background = self.canvas.create_image(self.master.winfo_screenwidth()/2,
                                self.master.winfo_screenheight()/2,
                                image=self.master.pages.get(self.master.pages_name[self.master.index]),
                                tag="app_background"
                                )
        #250, 690
        self.clickable_camera_button = self.canvas.create_image(self.master.winfo_screenwidth()/(768/125),
                                                                self.master.winfo_screenheight()/(144/115),
                                                                image=self.master.camera,
                                                                tag="camera_click")
        self.canvas.tag_bind(self.clickable_camera_button,
                             "<Button-1>", self.take_camera)
        self.is_hover_message_running = False
        # messages intéractions
        self.tool_tip_cam = HoverMessage(self.canvas, self.clickable_camera_button)
        create_hover_message(self.master, self.canvas, self.tool_tip_cam,
                             self.clickable_camera_button,
                             text="[Click Gauche]") # prendre caméra
        self.door_handle = HoverMessRelPos(self.master, self.canvas,
                                           "[Click gauche] pour ouvrir la porte")
        self.draw = HoverMessRelPos(self.master, self.canvas,
                                    "[E] pour dessiner")
        self.orange_kitchen = HoverMessRelPos(self.master, self.canvas,
                                              "[Click gauche] pour mieux observer")
        self.drawer_open = HoverMessRelPos(self.master, self.canvas,
                                           "[Click gauche] pour observer le tiroir")
        self.read_pamphlet_drawer = HoverMessRelPos(self.master, self.canvas,
                                                 "[E] pour lire la brochure")
        self.popup_draw = HoverMessRelPos(self.master, self.canvas,
                                          "[Click gauche] pour observer le bureau")
        self.see_books = HoverMessRelPos(self.master, self.canvas,
                                         "[Click gauche] pour regarder les livres")
        self.open_family_book = HoverMessRelPos(self.master, self.canvas,
                                                "[Click gauche] pour prendre le livre")
        self.camera = self.canvas.create_image(self.master.winfo_screenwidth()/2,
                                               self.master.winfo_screenheight()/1.5,
                                               image=self.master.camera
                                               )
        self.album = self.canvas.create_image(self.master.winfo_screenwidth() / 2,
                                              self.master.winfo_screenheight() / 2,
                                              image=self.master.album
                                              )
        self.change_page_to_left_arrow = self.canvas.create_image(560, 560,
                                              image=self.master.left_arrow, state="hidden"
                                            )
        self.change_page_to_right_arrow = self.canvas.create_image(975, 560,
                                              image=self.master.right_arrow, state="hidden"
                                            )
        self.canvas.tag_bind(self.change_page_to_left_arrow,
                             "<Button-1>", self.change_page_left)
        self.canvas.tag_bind(self.change_page_to_right_arrow,
                             "<Button-1>", self.change_page_right)
        self.images_pic_reference = []
        self.canvas.itemconfigure("camera_click", state="hidden")
        self.canvas.itemconfigure(self.album, state="hidden")
        self.canvas.itemconfigure(self.camera, state="hidden")
        self.dialog_box = open_image_setup_file("./images/intro/NB_RedBarTest.png")
        self.page_num = 1
        self.photos_list = []
        self.photos_list_updated = [] # sert à check si la liste a changé
        self.segmented_4_indexes_photos_list_updated = []
        self.sbarv = tk.Scrollbar(self, orient=VERTICAL)
        self.sbarh = tk.Scrollbar(self, orient=HORIZONTAL)
        self.sbarv.config(command=self.canvas.yview)
        self.sbarh.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=self.sbarv.set)
        self.canvas.config(xscrollcommand=self.sbarh.set)

        self.canvas.grid(row=0,column=0,sticky="NSEW")
        self.sbarv.grid(row=0,column=1,stick="NS")
        self.sbarh.grid(row=1,column=0,sticky="EW")
        self.rect = None
        self.start_x = None
        self.start_y = None
        # numéro pour id de la première image de la liste des photos
        self.initial_img_id = 0

    def on_button_press(self, event):
        """
        Enregistre coords initial souris
            - si pas de rect (cadre photo), création avec coords initial
        """
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y,
                                                     1, 1, outline='yellow', dash=(1,2))

    def on_move_press(self, event):
        """
        Appelle func après <Button-3> souris bouge
            - cur_x/cur_y = update
            - rectangle créé à partir de coords
        """
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        # agrandi rectangle pendant sélection
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_released(self, event=None):
        """
        Appelle func quand <Button-3> relâché (=photo prise)
            - appelle func place_photos_album_list
            - cur_x/cur_y (coords photos prises)
            - delete cadre photo
            - self.rect = None
        """
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.place_photo_album_list((self.start_x, self.start_y, cur_x, cur_y))
        self.master.game_e_handler.check_start_x = self.start_x
        self.master.game_e_handler.check_start_y = self.start_y
        self.master.game_e_handler.check_end_x = cur_x
        self.master.game_e_handler.check_end_y = cur_y
        self.canvas.delete(self.rect)
        self.rect = None
        self.master.check_game_events()
        # check si photo encadre posi° monstre
        self.master.game_e_handler.check_monster_taken_by_camera()
        # reset valeur check
        self.master.game_e_handler.check_start_x = 0
        self.master.game_e_handler.check_end_x = 0
        self.master.game_e_handler.check_start_y = 0
        self.master.game_e_handler.check_end_y = 0

    def hightlight_items(self, image, event=None):
        """
        WIP Func, encadré en jaune autour obj. utilisables
        """
        pass
        # print(self.canvas.itemconfigure(self.clickable_camera_button))
        # self.canvas.itemconfigure(image, activeimage="yellow")

    def take_camera(self, event=None):
        """
        Intéraction caméra-joueur
            - image caméra = détruise
            - caméra "de base" --> normal
        """
        self.canvas.delete(self.clickable_camera_button)
        self.canvas.itemconfigure(self.camera, state="normal")
        self.master.game_e_handler.camera_deleted = True
        self.master.game_e_handler.is_camera_available = True
        # click droit
        self.canvas.bind("<Button-3>", self.on_button_press)
        self.canvas.bind("<B3-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-3>", self.on_button_released)
        self.tool_tip_cam.hidetip()
        self.master.check_game_events()

    def open_album(self, event=None):
        """
        Ouvre album photos
            - si album = hidden
                - hidden --> normal
                - boutons flèche gauche/droite album --> normal
                - check si nv. photos prises
                - montre images page demandée
        """
        state = self.canvas.itemcget(self.album, "state")
        if state == "hidden":
            self.changing_state_canvas_item(self.album, "normal")
            self.changing_state_canvas_item(self.change_page_to_left_arrow, "normal")
            self.changing_state_canvas_item(self.change_page_to_right_arrow, "normal")
            self.is_album_photos_updated()
            self.show_pics_by_page_num(self.page_num)
        elif state == "normal":
            self.changing_state_canvas_item(self.album, "hidden")
            self.changing_state_canvas_item(self.change_page_to_left_arrow, "hidden")
            self.changing_state_canvas_item(self.change_page_to_right_arrow, "hidden")
            self.hide_photos_album()

    def changing_state_canvas_item(self, canvas_item_id, new_state):
        """
        Raccourci func itemconfigure pour changer state obj. "canevas"
        """
        self.canvas.itemconfigure(canvas_item_id, state=new_state)

    def change_is_running_value(self):
        """
        Stop de recréation mess. pop-up quand déjà crée (délai)
        """
        self.is_hover_message_running = not self.is_hover_message_running

    def place_photo_album_list(self, crop_dimensions):
        """
        Ajoute photo prise dans liste
            - image redimensionnée à image de tt écran
            - image "coupée" à zone délimitée par <Button-3> (click droit)
            - ref image gardée dans images_pic_reference
            - image créée (=photo prise) --> hidden
            - ajoue image dans photos_list_updated
        """
        # ajoute photo prise dans liste des photos
        image_to_crop_temp = Image.open(self.master.pages_file_location.get(self.master.pages_name[self.master.index]))
        image_to_crop = image_to_crop_temp.resize((screen_width,screen_height)).convert("RGBA")
        pic_size_in_album = (int(screen_width/8), int(screen_height/7))
        pic_taken_temp = image_to_crop.crop(crop_dimensions).resize(pic_size_in_album)
        pic_taken = ImageTk.PhotoImage(pic_taken_temp, master=self.master)
        self.images_pic_reference.append(pic_taken)
        image_id = self.canvas.create_image(
            0, 0,
            image=pic_taken,state="hidden"
        )
        self.photos_list_updated.append(image_id)

    def is_album_photos_updated(self, event=None):
        """
        Check si photos récentes prises:
            - crée un set avec photos prises (récentes)
            - crée un set avec photos prises (vielles)
            - si les 2 sets (=équivalents) --> ne fait rien
            - si les 2 sets (=diff.):
                - set vielles photos s'update
                - Reproduction d'une nv. liste de photos
        """
        updated_photos_set = set(self.photos_list_updated)
        current_photos_set = set(self.photos_list)
        diff = updated_photos_set.difference(current_photos_set)
        if diff:
            # print("SOMETHING HAS CHANGED")
            self.photos_list = self.photos_list_updated[:]
            self.listing_photos()
        else:
            # print("NOTHING HAS CHANGED")
            pass

    def listing_photos(self, event=None):
        """
        Crée image pour chaque photo dans album => grid
        """
        max_num_pics = 4
        self.segmented_4_indexes_photos_list_updated=\
            [self.photos_list[i:i + max_num_pics] for i in range(0, len(self.photos_list), max_num_pics)]

    def change_background(self, tag_or_id, new_background):
        """
        Raccourci func pour changer image fond d'écran
        """
        self.canvas.itemconfigure(tag_or_id, image=new_background)
        self.master.game_e_handler.get_current_room_img() # check reset_val quand souris bouge pas

    def change_page_left(self, event=None):
        """
            - Check si n° page > 1:
                - si oui, n° page - 1
                - Photos présentes pages droites (normal --> hidden)
                - Check si photos récentes prises
                - Photos présentes page demandée (hidden --> normal)
        """
        if self.page_num > 1:
            self.hide_photos_album()
            self.page_num -= 1
            self.is_album_photos_updated()
            self.show_pics_by_page_num(self.page_num)

    def change_page_right(self, event=None):
        """
            - Photos présentes pages gauche (normal --> hidden)
            - Ajoute n° page + 1
            - Check si photos récentes prises
            - Photos présentes page demandée (hidden --> normal)
        """
        self.hide_photos_album()
        self.page_num += 1
        self.is_album_photos_updated()
        self.show_pics_by_page_num(self.page_num)

    def get_bg_att(self, event=None):
        """
        Return "canvas object" avec le tag "app_background
        """
        return self.canvas.itemconfigure("app_background")

    def get_key_val_canvas_obj(self, obj, key):
        """
        Raccourci pour built-in func itemcget
        """
        return self.canvas.itemcget(obj, key)

    def show_pics_by_page_num(self, page_num):
        """
            - for loop toutes les photos d'une page précise
            - photos (hidden --> normal) et (normal --> hidden) sur ouverture album
            - max 4 photos par pages
            - change state que de 4 photos max
            - recrée une nouvelle liste index_segmented_list si joueur prend nv. photo
        """
        print(f"This is page {page_num}")
        index_segmented_list = page_num-1
        if len(self.segmented_4_indexes_photos_list_updated) != 0:
            try:
                current_pics_on_album = self.segmented_4_indexes_photos_list_updated[index_segmented_list]
                for index, pic in enumerate(current_pics_on_album):
                    print(pic, index)
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

    def hide_photos_album(self, event=None):
        """
        Photos présentes sur les 2 pages (normal --> hidden)
        """
        index_list = self.page_num-1
        print(index_list)
        if len(self.segmented_4_indexes_photos_list_updated) != 0:
            try:
                for pic in self.segmented_4_indexes_photos_list_updated[index_list]:
                    self.changing_state_canvas_item(pic, "hidden")
                    print(self.canvas.itemcget(pic, "state"))
            except IndexError:
                pass

    def create_dialog_box(self, chosen_moment, color="white"):
        """
            - crée sur demande texte à display selon actions/moments joueur
            - détruit texte à display après fin texte
        """
        # position texte
        dialog_position = (self.master.winfo_screenwidth()/2, self.master.winfo_screenheight()/1.25)
        # choisit texte à display selon action/moment joueur
        chosen_text = self.master.dial.dialog_to_use(chosen_moment)
        # texte = positionné au centre de black_dialog_bar
        dialog_text = self.canvas.create_text(
            (dialog_position[0], dialog_position[1]),
            text="", fill=color, font=("Helvetica", 15, "italic"))
        self.master.dial.typewritten_effect(dialog_text, chosen_text)


class Monster:
    """
    Classe gérant monstre:
        - "active" uniquement dès que self.monster_has_appeared = True
        - position monstre
        - image monstre
        - musique apparition monstre
    """
    def __init__(self, master):
        self.master = master
        # self.monster_design_img = [open_image_setup_file("images/monster/monster design/PA_NB_MonsterDesign.png"),
        #                            open_image_setup_file(""),
        #                            open_image_setup_file(""),
        #                            open_image_setup_file(""),
        #                            open_image_setup_file(""),
        #                            open_image_setup_file(""),
        #                            open_image_setup_file(""),
        #                            ]
        self.monster_design_img = [open_image_setup_file("images/monster/monster design/PA_NB_MonsterDesign.png"),
                                   open_image_setup_file("images/monster/monster design/PA_NB_MonsterDesign2.png")
                                   ]
        self.monster_design = None
        self.monster_timer = None
        self.is_monster_hunting = False
        self.monster_sound = pygame.mixer.Sound("./son/MonsterMusic.mp3")

    def show_monster(self):
        """
        Monstre apparaît sur l'écran (pièce où se trouve joueur)
        """
        index = randrange(len(self.monster_design_img))
        x = randrange(int(screen_width-screen_width/100))
        y = randrange(int(screen_height-screen_height/200))
        self.monster_design = self.master.rect.canvas.create_image(x, y, image=self.monster_design_img[index])
        # toggle monstre
        self.is_monster_hunting = True
        # musique monstre
        music.pause()
        monster_music.play(self.monster_sound)
        monster_music.set_volume(0.4)
        monster_music_length = self.monster_sound.get_length()+0.3   # 0.3 = marge de sécurité
        # timer pour tuer joueur
        self.monster_timer = threading.Timer(monster_music_length, self.kill_player)
        self.monster_timer.start()

    def hide_monster(self):
        """
        Monstre disparaît de la pièce où se trouve joueur
        """
        music.unpause()
        self.is_monster_hunting = False
        self.monster_timer.cancel()
        self.master.rect.canvas.delete(self.monster_design)

    def kill_player(self):
        """
        Tue le joueur
            - affiche écran de mort
            - revient à écran d'accueil
        """
        # cache monstre
        self.master.rect.canvas.delete(self.monster_design)
        # cache caméra en main
        self.master.rect.changing_state_canvas_item(self.master.rect.camera, "hidden")
        # attend pour action (ex: bouton) de l'écran de mort
        self.master.rect.change_background("app_background", self.master.death_screen)
        # relance programme
        self.master.rect.canvas.bind("<Button-1>", self.restart)

    def restart(self, event=None):
        """
        Relance programme en entier
        """
        global restart
        restart = True
        self.master.destroy()


def main():
    """
    Main func pour lancement programme(tkinter)
    """
    global restart
    root = App()
    HomeScreen(root)
    # code en-dessous uniquement atteignable si fenêtre self.master = détruite
    if restart == True:
        os.system('python "C:/Users/alpha/MyCode/Python Scripts/TM/mon_nom_est/mon_nom_est.py"')    # relance fichier

if __name__ == '__main__':
    main()
