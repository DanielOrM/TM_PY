from dialog.txt_files_reader import txt_files_reader
import time


class DialogBoxes:
    def __init__(self, master):
        self.master = master
        self.prev_text = ""
        self.index_letter = 0
        self.index_line = 0
        self.text = {
            "intro": txt_files_reader("dialog/dialog_text/intro_text.txt"),
            "camera_trouvee": txt_files_reader("dialog/dialog_text/camera_trouvee.txt"),
            "réveil": txt_files_reader("dialog/dialog_text/réveil.txt")
        }

    def typewritten_effect(self, text_id, chosen_text):
        # under the hood: appelle func change text
        self.change_text(text_id, self.prev_text, chosen_text)

    def change_text(self, tagOrId, new_text, chosen_text):
        # update le texte
        # print(self.prev_text)
        # print(new_text)
        # print(self.prev_text)
        # print(self.index_letter)
        # print(self.index_line)
        # print(self.prev_text)
        if self.prev_text:
            new_text = str(self.prev_text+new_text)
        # new_text = str(self.prev_text + new_text)
        self.master.rect.canvas.itemconfigure(tagOrId, text=new_text)
        self.prev_text = new_text
        # appelle func text_iteration après 300 ms
        self.master.after(80, self.text_iteration, tagOrId, chosen_text)

    def text_iteration(self, tagOrId, chosen_text):
        # print("Le texte se fait iterate...")
        # iterate à travers texte choisi et update le new_text dans func change_text
        # iterable_list = list(chosen_text)
        # iterable_list = list(line) # ligne = iterable
        try:
            iterable_line = list(chosen_text[self.index_line])
            # last_index_iterable_line = len(iterable_line)-1
            # print(iterable_list)
            try:
                new_letter = iterable_line[self.index_letter] # return la prochaine lettre dans le texte choisi
                # print(new_letter)
                if new_letter == "[":
                    print("STOP")
                    self.index_line = 0
                    self.index_letter = 0
                    self.prev_text = ""
                    # print(f"Ici c'est le reste: {self.prev_text}")
                    # time.sleep(1.5)
                    # attends 1,5s avant clear texte pour que joueur puisse lire
                    self.master.after(1500, self.master.rect.canvas.itemconfigure(tagOrId, text=""))
                    self.master.check_game_events() # vérifie events jeu à la fin du dialogue
                    # print(self.master.rect.canvas.itemcget(tagOrId, "text"))
                # elif new_letter == "." and iterable_line[self.index_letter+1] == "." \
                #         and iterable_line[self.index_letter+2] == "." and iterable_line[self.index_letter+3] == " " \
                #         and iterable_line[self.index_letter-1] == " ":
                #     self.prev_text = ""
                else:
                    self.change_text(tagOrId, new_letter, chosen_text)  # new_letter = new_text
                    self.index_letter += 1
            except IndexError:
                print("HA J'ai attrapé l'erreur")
                    # check_letter = iterable_line[self.index_letter]
                    # check_letter_2 = iterable_line[self.index_letter+1]
                    # check_letter_3 = iterable_line[self.index_letter+2]
                    # print(check_letter, check_letter_2, check_letter_3)
                if all(character == "." for character in list(chosen_text[self.index_line+1])):
                    time.sleep(1.5)
                    self.prev_text = ""
                    print("ça se vide...")
                    # self.index_line += 1
                    # self.index_letter = 0
                    # self.text_iteration(tagOrId, chosen_text)
                    # print("FINIIIIII C'est tout propre.")
                    # self.prev_text = ""
                # print(self.master.rect.canvas.itemcget(tagOrId, "text"))
                if self.master.rect.canvas.itemcget(tagOrId, "text") == " ...":
                    # print("Normalement ça marche.")
                    time.sleep(0.9)
                    self.prev_text = ""
                if len(self.master.rect.canvas.itemcget(tagOrId, "text")) > 50: # clear le texte s'il y a trop de caractères
                    self.prev_text = ""
                self.index_line += 1
                self.index_letter = 0
                # check_letter = iterable_line[self.index_letter]
                # check_letter_2 = iterable_line[self.index_letter+1]
                # check_letter_3 = iterable_line[self.index_letter+2]
                self.prev_text += " "
                time.sleep(0.5)
                self.text_iteration(tagOrId, chosen_text)
        except IndexError:
            return

    def dialog_to_use(self, chosen_moment):
        # choisit quel texte à return
        return self.text.get(chosen_moment)


