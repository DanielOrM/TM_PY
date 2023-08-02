from tkinter import *


class HoverMessage(object):
    def __init__(self, widget, item):
        self.widget = widget
        self.item = item
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text, event):
        "Display text in tooltip window"
        cx = self.widget.canvasx(event.x)
        cy = self.widget.canvasy(event.y)
        self.text = text
        if self.tipwindow or not self.text:
            return
        item_tag = self.widget.itemcget(self.item, "tags")
        # x, y, cx, cy = self.widget.bbox(item_tag)
        self.widget.coords(item_tag, self.x, self.y, cx, cy)
        x = self.x + cx
        y = self.y + cy
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def create_hover_message(master, widget, item, text):
    toolTip = HoverMessage(widget, item)

    def enter(event):
        is_running = master.rect.is_hover_message_running
        if not is_running:
            toolTip.showtip(text, event)
            master.rect.change_is_running_value()
            master.after(400, master.rect.change_is_running_value)

    def leave(event):
        toolTip.hidetip()

    widget.tag_bind(item, '<Leave>', leave)
    widget.tag_bind(item, '<Enter>', enter)







