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
            "preuve_parnm_oranges": txt_files_reader("dialog/dialog_text/preuve_parnm_oranges.txt")
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
        # print(self.prev_text)
        # print(new_text)
        # print(self.prev_text)
        # print(self.index_letter)
        # print(self.index_line)
        # print(self.prev_text)
        if self.prev_text:
            new_text = str(self.prev_text+new_text)
        # new_text = str(self.prev_text + new_text)
        self.master.rect.canvas.itemconfigure(tag_or_id, text=new_text)
        self.prev_text = new_text
        # appelle func text_iteration après 80 ms
        self.master.after(80, self.text_iteration, tag_or_id, chosen_text)

    def text_iteration(self, tag_or_id, chosen_text):
        """
        Itère travers texte choisi + update le new_text dans func change_text
        """
        if not self.is_running:
            # print("RETURN STATEMENT")
            self.is_running = True
            self.master.rect.canvas.itemconfigure(tag_or_id, text="")
            return
        try:
            iterable_line = list(chosen_text[self.index_line])
            # last_index_iterable_line = len(iterable_line)-1
            # print(iterable_list)
            try:
                # obtient prochaine lettre dans le texte choisi
                new_letter = iterable_line[self.index_letter]
                # print(new_letter)
                if new_letter == "[":
                    # print("STOP")
                    self.index_line = 0
                    self.index_letter = 0
                    self.prev_text = ""
                    # print(f"Ici c'est le reste: {self.prev_text}")
                    # time.sleep(1.5)
                    # attends 1,5s avant clear texte pour que joueur puisse lire
                    self.master.after(1500,
                                      self.master.rect.canvas.itemconfigure(tag_or_id, text=""))
                    self.master.check_game_events() # vérifie events jeu à la fin du dialogue
                else:
                    self.update_text(tag_or_id, new_letter, chosen_text)  # new_letter = new_text
                    self.index_letter += 1
            except IndexError:
                if all(character == "." for character in list(chosen_text[self.index_line+1])):
                    time.sleep(1.5)
                    self.prev_text = ""
                    # print("ça se vide...")
                if self.master.rect.canvas.itemcget(tag_or_id, "text") == " ...":
                    # print("Normalement ça marche.")
                    time.sleep(0.9)
                    self.prev_text = ""
                # clear le texte s'il y a trop de caractères
                if len(self.master.rect.canvas.itemcget(tag_or_id, "text")) > 50:
                    self.prev_text = ""
                self.index_line += 1
                self.index_letter = 0
                # check_letter = iterable_line[self.index_letter]
                # check_letter_2 = iterable_line[self.index_letter+1]
                # check_letter_3 = iterable_line[self.index_letter+2]
                self.prev_text += " "
                time.sleep(0.5)
                self.text_iteration(tag_or_id, chosen_text)
        except IndexError:
            return

    def dialog_to_use(self, chosen_moment):
        """
        Choisit quel texte à return
        """
        return self.text.get(chosen_moment)

    def stop(self):
        # print("Still RUNNING")
        self.is_running = False
        self.prev_text = ""
        self.index_letter = 0
        self.index_line = 0
