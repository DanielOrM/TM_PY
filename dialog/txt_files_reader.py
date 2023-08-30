"""Fonction pour textes (dialogue)"""


def txt_files_reader(text_to_read):
    """
    Facilite l'identation si les textes sont longs
    """
    # print(text_to_read)
    with open(text_to_read, mode="r", encoding="utf-8") as file:
        # whole_text = ""
        lines = [line.rstrip('\n') for line in file]
        # for line in lines:
        #     whole_text += line
        # print(whole_text)
        # print(lines[1])
        return lines
