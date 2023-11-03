"""
Textes affichés "dialogues"
Problèmes principale: time.sleep car peut faire bugguer d'autres func
"""
import time
from dialog.txt_files_reader import txt_files_reader


class DialogBoxes:
    """
    Évenements:
        - affiche texte à choix en bas de l'écran
        - effet "d'écriture" pour textes affichés
        - Itère texte par ligne et par lettre
    """
    def __init__(self, master):
        self.master = master
        self.prev_text = ""
        self.index_letter = 0
        self.index_line = 0
        self.is_running = True
        self.text = {
            "intro": txt_files_reader("dialog/dialog_text/intro_text.txt"),
            "camera_trouvee": txt_files_reader("dialog/dialog_text/camera_trouvee.txt"),
            "réveil": txt_files_reader("dialog/dialog_text/réveil.txt"),
            "porte_essai": txt_files_reader("dialog/dialog_text/porte_essai.txt"),
            "porte_essai_2": txt_files_reader("dialog/dialog_text/porte_essai_2.txt"),
            "preuve_parnm_oranges": txt_files_reader("dialog/dialog_text/preuve_parnm_oranges.txt"),
            "player_room": txt_files_reader("dialog/dialog_text/player_room.txt"),
            "découverte_cahier_dessin": txt_files_reader("dialog/dialog_text/découverte_cahier_dessin.txt"),
            "dessins": txt_files_reader("dialog/dialog_text/dessins.txt")
        }

    def typewritten_effect(self, text_id, chosen_text):
        """
        Under the hood: appelle func update_text
        """
        self.update_text(text_id, self.prev_text, chosen_text)

    def update_text(self, tag_or_id, new_text, chosen_text):
        """
        Update le texte à intervalles
        """
        if self.prev_text:
            new_text = str(self.prev_text+new_text)
        self.master.rect.canvas.itemconfigure(tag_or_id, text=new_text)
        self.prev_text = new_text
        # appelle func text_iteration après 60 ms
        self.master.after(60, self.text_iteration, tag_or_id, chosen_text)

    def text_iteration(self, tag_or_id, chosen_text):
        """
        Itère travers texte choisi + update le new_text dans func change_text
        """
        if not self.is_running:
            self.is_running = True
            self.master.rect.canvas.itemconfigure(tag_or_id, text="")
            return
        try:
            iterable_line = list(chosen_text[self.index_line])
            try:
                # obtient prochaine lettre dans le texte choisi
                new_letter = iterable_line[self.index_letter]
                if new_letter == "[":
                    # marque fin dialogue
                    self.index_line = 0
                    self.index_letter = 0
                    self.prev_text = ""
                    # attends 1,2s avant clear texte pour que joueur puisse lire
                    self.master.after(1200,
                                      self.master.rect.canvas.itemconfigure(tag_or_id, text=""))
                    self.master.check_game_events() # vérifie events jeu à la fin du dialogue
                else:
                    self.update_text(tag_or_id, new_letter, chosen_text)  # new_letter = new_text
                    self.index_letter += 1
            except IndexError:
                if all(character == "." for character in list(chosen_text[self.index_line+1])) \
                        and chosen_text[self.index_line] != "":
                    # reset le texte visible après 1150 ms
                    self.master.after(1150, self.reset_prev_text)
                if self.master.rect.canvas.itemcget(tag_or_id, "text") == " ...":
                    # reset le texte visible après 800 ms
                    self.master.after(800, self.reset_prev_text)
                # clear le texte s'il y a trop de caractères
                if len(self.master.rect.canvas.itemcget(tag_or_id, "text")) > 50:
                    self.prev_text = ""
                self.index_line += 1
                self.index_letter = 0
                self.prev_text += " "
                # recommence la loop après 900 ms
                self.master.after(900, self.text_iteration, tag_or_id, chosen_text)
        except IndexError:
            return

    def dialog_to_use(self, chosen_moment):
        """
        Choisit quel texte à return
        """
        return self.text.get(chosen_moment)

    def reset_prev_text(self):
        """
        Assigne attribut "self.prev_text" à une string vide
        """
        self.prev_text = ""

    def stop(self):
        """
        Dialog fini, reset
        """
        self.is_running = False
        self.prev_text = ""
        self.index_letter = 0
        self.index_line = 0
