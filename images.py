from tkinter import PhotoImage, Label


def bg_image_setup(file_location):
    bg_image = PhotoImage(file=file_location)
    return bg_image


def set_bg(parent, bg_image):
    background_label = Label(parent, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
