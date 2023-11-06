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


def open_and_resize_img(file_location, name, x, y):
    """
    Ouvre image et la redimensionne
    """
    image = Image.open(file_location)
    bg_image = ImageTk.PhotoImage(image.resize((x, y)), name=name)
    return bg_image


def bg_image_setup(file_location, name):
    """
    Return image resize au plein écran [Image/ImageTk]
    """
    bg_image = open_and_resize_img(file_location, name, screen_width, screen_height)
    return bg_image
