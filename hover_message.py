"""
Module Tk
messages pop-up avec une image existante
"""
from tkinter import Toplevel, Label, LEFT, SOLID


class HoverMessage:
    """
    Classe qui crée toutes les func: --> image
        - showtip
        - hidetip
    """
    def __init__(self, widget, item):
        self.widget = widget
        self.text = None
        self.item = item
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text, event):
        """
        Texte dans un canvas (rectangle)
        """
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
        """
        Cache texte + canvas (rectangle)
        """
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def create_hover_message(master, widget, tool_tip, item, text):
    """
    Sert à appeler func tout HoverMessage
    """

    def enter(event):
        is_running = master.rect.is_hover_message_running
        if not is_running:
            tool_tip.showtip(text, event)
            master.rect.change_is_running_value()
            master.after(250, master.rect.change_is_running_value)

    def leave(event=None):
        tool_tip.hidetip()

    widget.tag_bind(item, '<Leave>', leave)
    widget.tag_bind(item, '<Enter>', enter)





class CreateHoverMessRelPos:
    """
    Hover message quand la souris est à une position précise
    """
    def __init__(self, widget):
        self.widget = widget
        self.text = None
        self.tip_window = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text, event):
        """
        Texte dans un canvas (rectangle)
        """
        cx = self.widget.canvasx(event.get("x"))
        cy = self.widget.canvasy(event.get("y"))
        self.text = text
        if self.tip_window or not self.text:
            return
        # x, y, cx, cy = self.widget.bbox(item_tag)
        x = self.x + cx
        y = self.y + cy
        self.tip_window = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        # label.place(x=event.get("x"), y=event.get("y"))
        label.pack(ipadx=1)

    def hidetip(self, event=None):
        """
        Cache texte + canvas (rectangle)
        """
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


class HoverMessRelPos:
    """
    Classe qui crée toutes les func: --> pos. rel
        - showtip
        - hidetip
    """
    def __init__(self, master, widget, text):
        self.master = master
        self.widget = widget
        self.text = text
        self.pop_up = CreateHoverMessRelPos(widget)

    def show_tip(self, event):
        """
        Texte dans un canvas (rectangle)
        """
        is_running = self.master.rect.is_hover_message_running
        if not is_running:
            self.pop_up.showtip(self.text, event)
            self.master.rect.change_is_running_value()
            self.master.after(250, self.master.rect.change_is_running_value)

    def hide_tip(self, event=None):
        """
        Cache texte + canvas (rectangle)
        """
        self.pop_up.hidetip()
