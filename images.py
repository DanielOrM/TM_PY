"""Module utilisé pour importer PhotoImage (resize)"""
from tkinter import PhotoImage
from PIL import ImageTk, Image
from global_var import screen_width, screen_height


def open_image_setup_file(file_location):
    """
    Return une image d'après fichier [PhotoImage]
    """
    image = PhotoImage(file=file_location)
    return image


def bg_image_setup(file_location, name):
    """
    Return image resize au plein écran [Image/ImageTk]
    """
    # bg_image = PhotoImage(file=file_location)
    bg_image_temp = Image.open(file_location)
    bg_image = ImageTk.PhotoImage(bg_image_temp.resize((screen_width, screen_height)), name=name)
    return bg_image


# def set_bg(parent, bg_image):
#     background_label = Label(parent, image=bg_image)
#     background_label.place(x=0, y=0, relwidth=1, relheight=1)
