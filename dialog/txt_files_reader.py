# facilite l'identation si les textes sont longs
def txt_files_reader(text_to_read):
    # print(text_to_read)
    with open(text_to_read, mode="r", encoding="utf-8") as f:
        # whole_text = ""
        lines = [line.rstrip('\n') for line in f]
        # for line in lines:
        #     whole_text += line
        # print(whole_text)
        # print(lines)
        return lines