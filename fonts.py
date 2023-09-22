from PIL import ImageFont, ImageDraw, Image


class RenderFont:
    def __init__(self, master, filename, fill=(0, 0, 0)):
        """
        constructor for RenderFont
        filename: the filename to the ttf font file
        fill: the color of the text
        """
        self.master = master
        self._file = filename
        self._fill = fill
        self._image = None
        self._image_temp = None

    def get_render(self, font_size, txt, type_="normal"):
        """
        returns a transparent PIL image that contains the text
        font_size: the size of text
        txt: the actual text
        type_: the type of the text, "normal" or "bold"
        """
        if type(txt) is not str:
            raise TypeError("text must be a string")

        if type(font_size) is not int:
            raise TypeError("font_size must be a int")

        width = len(txt) * font_size
        height = font_size + 5

        font = ImageFont.truetype(font=self._file, size=font_size)
        self._image_temp = Image.new(mode='RGBA', size=(width, height), color=(255, 255, 255))
        rgba_data = self._image_temp.getdata()
        newdata = []

        for item in rgba_data:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newdata.append((255, 255, 255, 0))
            else:
                newdata.append(item)

        self._image_temp.putdata(newdata)

        draw = ImageDraw.Draw(im=self._image_temp)

        if type_ == "normal":
            draw.text(xy=(width / 2, height / 2), text=txt, font=font, fill=self._fill, anchor='mm')
        elif type_ == "bold":
            draw.text(xy=(width / 2, height / 2), text=txt, font=font, fill=self._fill, anchor='mm',
                      stroke_width=1, stroke_fill=self._fill)
        # self._image = ImageTk.PhotoImage(self._image_temp, master=self.master.home_s)
        self.master.fonts_list.append(self._image_temp)
        self._image_temp.save("title.png", "PNG")
        return self._image_temp
