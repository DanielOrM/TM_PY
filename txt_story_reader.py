"""Importation de la fonction gérant le stockage de tout ce qui est écrit sur un fichier .txt en 1 string"""
from dialog.txt_files_reader import txt_files_story


def txt_story_reader(app, txt_file):
    """
    - Création bloc de texte gris clair
    - Valeur du texte = txt_file
    """
    # print("HEHEHEHEHEHEHEH")
    app.rect.changing_state_canvas_item(app.game_e_handler.text_box, "normal")
    app.rect.canvas.itemconfigure(app.game_e_handler.text_readable,
                                  text=txt_files_story(txt_file))
    app.rect.changing_state_canvas_item(app.game_e_handler.text_readable, "normal")


def reset_story_reader(app):
    app.rect.changing_state_canvas_item(app.game_e_handler.text_box, "hidden")
    app.rect.changing_state_canvas_item(app.game_e_handler.text_readable, "hidden")
