from tkinter import *

# hover message avec une image existante


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

    def hidetip(self, event=None):
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

    def leave(event=None):
        toolTip.hidetip()

    widget.tag_bind(item, '<Leave>', leave)
    widget.tag_bind(item, '<Enter>', enter)


# hover message quand la souris est à une position précise
class CreateHoverMessRelPos(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text, event):
        "Display text in tooltip window"
        cx = self.widget.canvasx(event.get("x"))
        cy = self.widget.canvasy(event.get("y"))
        self.text = text
        if self.tipwindow or not self.text:
            return
        # x, y, cx, cy = self.widget.bbox(item_tag)
        x = self.x + cx
        y = self.y + cy
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        # label.place(x=event.get("x"), y=event.get("y"))
        label.pack(ipadx=1)

    def hidetip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


class HoverMessRelPos:
    def __init__(self, master, widget, text):
        self.master = master
        self.widget = widget
        self.text = text
        self.pop_up = CreateHoverMessRelPos(widget)

    def show_tip(self, event):
        is_running = self.master.rect.is_hover_message_running
        if not is_running:
            self.pop_up.showtip(self.text, event)
            self.master.rect.change_is_running_value()
            self.master.after(400, self.master.rect.change_is_running_value)

    def hide_tip(self, event=None):
        self.pop_up.hidetip()

# def create_hover_mess_rel_pos(widget):
#     toolTip = HoverMessRelPos(widget)
#     return toolTip


# def enter(event, master, widget, text):
#     is_running = master.rect.is_hover_message_running
#     toolTip = create_hover_mess_rel_pos(widget)
#     if not is_running:
#         toolTip.showtip(text, event)
#         master.rect.change_is_running_value()
#         master.after(400, master.rect.change_is_running_value)


# def leave(widget):
#     toolTip = create_hover_mess_rel_pos(widget)
#     toolTip.hidetip()




