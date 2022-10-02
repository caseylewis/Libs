from tkinter import *
import platform
import pyperclip


########################################################################################################################
########################################################################################################################
#  WIDGET PLUS SECTION
#
# THIS SECTION IS WHERE ALL THE EXTENDED WIDGETS WILL BE DEFINED. SUCH AS:
#   - CheckbuttonPlus
#   - EntryPlus
#   - DropdownPlus
#   - LoggerPlus
#   - ScrollFramePlus
########################################################################################################################
# LOCAL STYLE DEFINITION
_title_args = {
    'bg': 'black',
    'fg': 'white',
    'font': ("Helvetica", 18)
}
########################################################################################################################
# LOCAL GRID DEFINITION
_grid_args = {
    'pady': 5,
    'padx': 5,
    'sticky': 'new',
}
########################################################################################################################


class CheckbuttonPlus(Checkbutton):
    ON = 1
    OFF = 0

    def __init__(self, root, default_val=OFF, select_func=None, deselect_func=None, *args, **kwargs):
        self._select_func = select_func
        self._deselect_func = deselect_func
        self._var = IntVar()
        self._var.trace('w', lambda x, y, z: self.__on_val_change())
        super().__init__(root, variable=self._var, *args, **kwargs)
        self._default_value = default_val

    def get(self):
        return self._var.get()

    def set(self, val):
        if val == 1:
            self._var.set(1)
        elif val == 0:
            self._var.set(0)
        else:
            raise Exception("CheckbuttonPlus does not support setting values other than 0 or 1.")

    def default(self):
        self.set(self._default_value)

    def __on_val_change(self):
        if self.get() == self.ON:
            if self._select_func is not None:
                self._select_func()
        else:
            if self._deselect_func is not None:
                self._deselect_func()


class EntryPlus(Entry):
    def __init__(self, root, default_text='', *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self._default_text = default_text
        self.default()

    def default(self):
        self.set(self._default_text)

    def clear(self):
        self.delete(0, END)

    def set(self, set_text):
        self.clear()
        self.insert(0, set_text)


class TextPlus(Text):
    def __init__(self, root, read_only=False, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        # SET THE READ ONLY STATUS TO WHATEVER VALUE IS PASSED
        self._read_only = None
        self.set_read_only(read_only)

    def set(self, text):
        """
        Handles Read-only.
        If read only:
            - clears read only
            - sets text
            - sets back to read only
        Else:
            - sets text
        """
        if self._read_only is True:
            self.__clear_read_only()
            self.__set_text(text)
            self.__make_read_only()
        else:
            self.__set_text(text)

    def clear(self):
        """
        Handles Read-only.
        If read only:
            - clears read only
            - deletes all text
            - sets back to read only
        Else:
            - deletes all text
        """
        if self._read_only is True:
            self.__clear_read_only()
            self.__delete_all()
            self.__make_read_only()
        else:
            self.__delete_all()

    def append(self, text):
        if self._read_only is True:
            self.__clear_read_only()
            self.__insert_end(text)
            self.__make_read_only()
        else:
            self.__insert_end(text)

    def set_read_only(self, value):
        if value is True:
            self.__make_read_only()
        else:
            self.__clear_read_only()

    def __make_read_only(self):
        self._read_only = True
        self.config(state=DISABLED)

    def __clear_read_only(self):
        self._read_only = False
        self.config(state=NORMAL)

    def __set_text(self, text):
        """
        Deletes all text, then inserts the text that was passed.
        """
        self.__delete_all()
        self.insert(END, text)

    def __delete_all(self):
        """
        Simple delete of all text.
        """
        self.delete('1.0', END)

    def __insert_end(self, text):
        """
        Simple insert of text at the END location.
        """
        self.insert(END, text)


class DropdownPlus(OptionMenu):
    def __init__(self, root, options_list=None, on_change_func=None, **kwargs):
        if options_list is None:
            self._options_list = ['Empty']
        else:
            self._options_list = options_list
        self.on_change_func = on_change_func

        self._var = StringVar(root)
        self._var.set(self._options_list[0])
        self._var.trace('w', lambda x, y, z: self.__on_change_callback())
        super().__init__(root, self._var, *self._options_list)

        # BY DEFAULT, MAKE HIGHLIGHTTHICKNESS 0, THEN IF USER CONFIGURES IT WILL OVERRIDE
        self.config(highlightthickness=0)
        # CONFIGURE USER PASSED SETTINGS
        self.config(**kwargs)

    def __on_change_callback(self):
        if self.on_change_func is not None:
            self.on_change_func()

    def __build_list(self, options_list):
        menu = self["menu"]
        menu.delete(0, "end")
        for string in options_list:
            menu.add_command(label=string, command=lambda value=string: self._var.set(value))

    def add_option(self, option):
        """
        Adds the option to the _options_list. Then, deletes everything from the list, and rebuilds it.
        """
        self._options_list.append(option)
        menu = self["menu"]
        menu.delete(0, "end")
        for string in self._options_list:
            menu.add_command(label=string, command=lambda value=string: self._var.set(value))

    def remove_option(self, option_string):
        """
        Searches the current option for the option_string, if found removes it. Then, clears the current list and
        rebuilds the list from what is left.
        """
        for option in self._options_list:
            if option_string == option:
                self._options_list.remove(option)

        menu = self["menu"]
        menu.delete(0, "end")
        for string in self._options_list:
            menu.add_command(label=string, command=lambda value=string: self._var.set(value))
        self.default()

    def set_options(self, options_list):
        """
        Sets the options to be exactly what is passed as options_list.
        Completely clears and sets a new list.
        """
        self._options_list = options_list

        menu = self["menu"]
        menu.delete(0, "end")
        for string in self._options_list:
            menu.add_command(label=string, command=lambda value=string: self._var.set(value))
        self.default()

    def default(self):
        try:
            self._var.set(self._options_list[0])
        except IndexError:
            print('list index out of range')

    def get(self):
        return self._var.get()

    def set(self, value):
        if value in self._options_list:
            self._var.set(value)


class LoggerPlus(Text):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.config(state=DISABLED)

    def log(self, message):
        self.config(state=NORMAL)
        self.insert(END, message)
        self.config(state=DISABLED)


class ScrollFramePlus(Frame):
    def __init__(self, root, hide_scrollbar=False, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        # CREATE A CANVAS OBJECT AND A VERTICAL SCROLLBAR FOR SCROLLING IT
        self._v_scrollbar = Scrollbar(self, orient=VERTICAL)
#         self._v_scrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        # ONLY SHOW SCROLL BAR IF ASKED FOR
        if hide_scrollbar is False:
            self._v_scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
        self._canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=self._v_scrollbar.set, bg='green')
        self._canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self._v_scrollbar.config(command=self._canvas.yview)

        # RESET THE VIEW
        self._canvas.xview_moveto(0)
        self._canvas.yview_moveto(0)

        # CREATE A FRAME INSIDE THE CANVAS WHICH WILL BE SCROLLED WITH IT
        self.view_port = interior = Frame(self._canvas, bg='blue')
        interior_id = self._canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self._canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != self._canvas.winfo_width():
                # update the self.canvas's width to fit the inner frame
                self._canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != self._canvas.winfo_width():
                # update the inner frame's width to fill the self.canvas
                self._canvas.itemconfigure(interior_id, width=self._canvas.winfo_width())
                # self.view_port.config(width=interior.winfo_reqwidth())
        self._canvas.bind('<Configure>', _configure_canvas)

        # SET EVENTS FOR ENTERING/LEAVING VIEWPORT
        self.view_port.bind('<Enter>', self.__on_enter)
        self.view_port.bind('<Leave>', self.__on_leave)

        self.config(**kwargs)

    def __on_mouse_wheel(self, event):
        # GET SCROLL VECTORS
        top, bottom = self._v_scrollbar.get()

        # IF SCROLLBAR IS MAXED OUT, DON'T ALLOW SCROLL
        if top == 0 and bottom == 1:
            return
        else:
            # PERFORM SCROLL
            if platform.system() == 'Windows':
                self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif platform.system() == 'Darwin':
                self._canvas.yview_scroll(int(-1 * event.delta), "units")
            else:
                if event.num == 4:
                    self._canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    self._canvas.yview_scroll(1, "units")

    def scroll_to(self, index):
        self.update_idletasks()
        self._canvas.yview_moveto(index)
        self.update()

    def __on_enter(self, event):  # bind wheel events when the cursor enters the control
        if platform.system() == 'Linux':
            self._canvas.bind_all("<Button-4>", self.__on_mouse_wheel)
            self._canvas.bind_all("<Button-5>", self.__on_mouse_wheel)
            self.view_port.bind_all("<Button-4>", self.__on_mouse_wheel)
            self.view_port.bind_all("<Button-5>", self.__on_mouse_wheel)
        else:
            self._canvas.bind_all("<MouseWheel>", self.__on_mouse_wheel)

    def __on_leave(self, event):  # unbind wheel events when the cursorl leaves the control
        if platform.system() == 'Linux':
            self._canvas.unbind_all("<Button-4>")
            self._canvas.unbind_all("<Button-5>")
        else:
            self._canvas.unbind_all("<MouseWheel>")

    def config(self, *args, **kwargs):
        # LIST OF ARGS TO APPLY TO CANVAS, NOT FRAME
        canvas_arg_list = [
            'width',
            'height',
            'highlightthickness',
            'highlightbackground',
        ]
        # DICT TO CONFIGURE CANVAS
        canvas_arg_dict = {}

        # ITERATE THROUGH KWARGS TO SEE WHICH KEYS NEED TO BE APPLIED TO CANVAS
        for key in kwargs.keys():
            if key in canvas_arg_list:
                canvas_arg_dict[key] = kwargs[key]

        # REMOVE THE KEYS FROM KWARGS THAT WERE PUT IN CANVAS DICT
        for key in canvas_arg_dict.keys():
            kwargs.pop(key)

        # CONFIGURE CANVAS
        self._canvas.configure(**canvas_arg_dict)
        # for key, value in canvas_arg_dict.items():
        #     print('canvas_dict', key, value)

        # CONFIGURE FRAME
        self.view_port.configure(**kwargs)
        self['bg'] = self.view_port['bg']
        # for key, value in kwargs.items():
        #     print('kwargs', key, value)

        # ENSURE CANVAS HIGHLIGHT IS THE SAME AS THE BACKGROUND
        self._canvas.configure(highlightbackground=self['bg'], bg=self['bg'])


########################################################################################################################
########################################################################################################################
#  EXTENDED WIDGET SECTION
#
# THIS SECTION IS WHERE ALL THE EXTENDED WIDGETS WILL BE DEFINED. SUCH AS:
#   - ButtonWithBorder
#   - LabelWithCopy
########################################################################################################################


class ButtonWithBorder(Frame):
    """
    Example args:
    button_with_copy_args = {
        'font_style': 'Times',
        'font_size': 18,
        'font_extras': 'italic',
        'bg': 'white',
        'fg': '#ff4d5b', # LIGHTRED
        'bd': 3
    }
    """
    def __init__(self, root, text, command,
                 font_style="Times",
                 font_size=12,
                 font_extras='',
                 bg="black",
                 fg="white",
                 bd=3):
        super().__init__(root)
        self.font_style = font_style
        self.font_size = font_size
        self.font_extras = font_extras
        self.bg = bg
        self.fg = fg
        self.bd = bd
        self.__command = command
        # FRAME BG MUST BE SET TO FG
        self.config(bg=self.fg)
        # CONFIGURE COLUMNS AND ROWS
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        font = f'{self.font_style} {self.font_size} {self.font_extras}'

        # LABEL
        self._btn = Button(self, text=text.upper(), command=self.__command, font=font, bg=self.bg, fg=self.fg, relief='flat')
        self._btn.grid(row=0, column=0, sticky='nsew', pady=self.bd, padx=self.bd)

        # CONFIGURE ENTER AND LEAVE
        self._btn.bind('<Enter>', self.__on_enter)
        self._btn.bind('<Leave>', self.__on_leave)

    def set(self, btn_text):
        """
        Sets the button text with the passed btn_text.
        """
        self._btn.config(text=btn_text)

    def __on_enter(self, event):
        self._btn.config(bg=self.fg, fg=self.bg)
        self.config(bg=self.bg)

    def __on_leave(self, event):
        self._btn.config(bg=self.bg, fg=self.fg)
        self.config(bg=self.fg)


class LabelWithCopy(Frame):
    """
    Example args:
    bordered_button_args = {
        'font_style': 'Times',
        'font_size': 18,
        'bg': 'black',
        'fg': 'white',
        'bd': 5
    }
    """
    _font_extras = 'bold'

    def __init__(self, root, lbl_text,
                 font_style="Times",
                 font_size=12,
                 bg="black",
                 fg="white",
                 bd=3
                 ):
        super().__init__(root)
        self.font_style = font_style
        self.font_size = font_size
        self.bg = bg
        self.fg = fg
        self.bd = bd
        # FRAME BG MUST BE SET TO FG
        self.config(bg=self.fg)
        # CONFIGURE COLUMNS AND ROWS
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        font = f'{self.font_style} {self.font_size} {self._font_extras}'

        # LABEL
        self._lbl = Label(self, text=lbl_text.upper(), font=font, bg=self.bg, fg=self.fg)
        self._lbl.grid(row=0, column=0, sticky='nsew', pady=self.bd, padx=(self.bd, 0))

        # COPY BUTTON
        copy_text = '✎'
        copy_text_width = len(copy_text) + 2
        self._copy_btn = Button(self, text=copy_text, font=font, bg=self.bg, fg=self.fg, width=copy_text_width, relief='flat', command=lambda: self.__copy_text_to_clipboard())
        self._copy_btn.grid(row=0, column=1, pady=self.bd, padx=self.bd, sticky='nsew')

    def __copy_text_to_clipboard(self):
        pyperclip.copy(self._lbl['text'])


class DropdownWithLabel(Frame):
    """
    Example args:
    _dropdown_with_label_args = {
        'font_style': 'Times',
        'font_size': 24,
        'bg': 'white',
        'fg': '#566069',
        'bd': 1,
        'label_font_size': 12,
    }
    """
    def __init__(self, root, lbl_text, options_list, on_change_func=None,
                 font_style="Times",
                 font_size=12,
                 bg="black",
                 fg="white",
                 bd=3,
                 label_font_size=8):
        super().__init__(root)
        self.config(bg=fg)

        class _Rows:
            LABEL = 0
            DROPDOWN = 1
        self.grid_rowconfigure(_Rows.LABEL, weight=1)
        self.grid_rowconfigure(_Rows.DROPDOWN, weight=0)

        class _Columns:
            MAIN = 0
        self.grid_columnconfigure(_Columns.MAIN, weight=1)
        self._label = Label(self, text=lbl_text, anchor=W, bg=bg, fg=fg, font=f"{font_style} {label_font_size}")
        self._label.grid(row=_Rows.LABEL, column=_Columns.MAIN, sticky='sew', pady=(0, 0), padx=(0, 0))
        self._dropdown = DropdownPlus(self, options_list=options_list, on_change_func=on_change_func, bg=bg, fg=fg, font=f"{font_style} {font_size}")
        self._dropdown.grid(row=_Rows.DROPDOWN, column=_Columns.MAIN, sticky='ew', pady=(0, bd), padx=(0, 0))

    def add_option(self, option):
        """
        Adds the option to the _options_list. Then, deletes everything from the list, and rebuilds it.
        """
        self._dropdown.add_option(option)

    def remove_option(self, option_string):
        """
        Searches the current option for the option_string, if found removes it. Then, clears the current list and
        rebuilds the list from what is left.
        """
        self._dropdown.remove_option(option_string)

    def set_options(self, options_list):
        """
        Sets the options to be exactly what is passed as options_list.
        Completely clears and sets a new list.
        """
        self._dropdown.set_options(options_list)

    def default(self):
        self._dropdown.default()

    def get(self):
        return self._dropdown.get()

    def set(self, value):
        self._dropdown.set(value)


class EntryWithLabel(Frame):
    """
    Example args:
    _entry_with_label_args = {
        'font_style': 'Times',
        'font_size': 24,
        'bg': 'white',
        'fg': '#566069',
        'bd': 1,
        'label_font_size': 12,
    }
    """
    def __init__(self, root, lbl_text, default_text="",
                 font_style="Times",
                 font_size=12,
                 bg="black",
                 fg="white",
                 bd=3,
                 label_font_size=8):
        super().__init__(root)
        self.config(bg=fg)
        self._default_text = default_text

        class _Rows:
            LABEL = 0
            ENTRY = 1
        self.grid_rowconfigure(_Rows.LABEL, weight=1)
        self.grid_rowconfigure(_Rows.ENTRY, weight=0)

        class _Columns:
            MAIN = 0
        self.grid_columnconfigure(_Columns.MAIN, weight=1)
        self._label = Label(self, text=lbl_text, anchor=W, bg=bg, fg=fg, font=f"{font_style} {label_font_size}")
        self._label.grid(row=_Rows.LABEL, column=_Columns.MAIN, sticky='sew', pady=(0, 0), padx=(0, 0))
        self._entry = EntryPlus(self, default_text=self._default_text, bg=bg, fg=fg, font=f"{font_style} {font_size}")
        self._entry.grid(row=_Rows.ENTRY, column=_Columns.MAIN, sticky='ew', pady=(0, bd), padx=(0, 0))

    def get(self):
        return self._entry.get()

    def default(self):
        self._entry.set(self._default_text)

    def clear(self):
        self._entry.delete(0, END)

    def set(self, set_text):
        self.clear()
        self._entry.insert(0, set_text)

    def focus_set(self):
        self._entry.focus_set()


class LabelWithLabel(Frame):
    """
    Example args:
    _label_with_label_args = {
        'font_style': 'Times',
        'font_size': 24,
        'bg': 'white',
        'fg': '#566069',
        'bd': 1,
        'label_font_size': 12,
    }
    """
    def __init__(self, root, text, lbl_text,
                 font_style="Times",
                 font_size=12,
                 bg="black",
                 fg="white",
                 bd=3,
                 anchor=W,
                 label_font_size=8):
        super().__init__(root)
        self._font_style = font_style
        self._font_size = font_size
        self._bg = bg
        self._fg = fg
        self._bd = bd
        self._anchor = anchor
        self._label_font_size = label_font_size

        # CONFIGURE FRAME
        self.configure(bg=fg)
        self._text = text

        class _Rows:
            LABEL = 0
            MAIN_LBL = 1
        self.grid_rowconfigure(_Rows.LABEL, weight=1)
        self.grid_rowconfigure(_Rows.MAIN_LBL, weight=0)

        class _Columns:
            MAIN = 0
        self.grid_columnconfigure(_Columns.MAIN, weight=1)

        # LABEL
        self._label = Label(self, text=lbl_text)
        self._label.grid(row=_Rows.LABEL, column=_Columns.MAIN, sticky='sew', pady=(0, 0), padx=(0, 0))
        self.configure_lbl(font_style=self._font_style, label_font_size=self._label_font_size, bg=self._bg, fg=self._fg, anchor=self._anchor)
        # MAIN LABEL
        self._main_lbl = Label(self, text=self._text)
        self._main_lbl.grid(row=_Rows.MAIN_LBL, column=_Columns.MAIN, sticky='ew')
        self.configure_main_lbl(font_style=self._font_style, font_size=self._font_size, bg=self._bg, fg=self._fg, bd=self._bd, anchor=self._anchor)

    def get(self):
        return self._main_lbl['text']

    def set(self, set_text):
        self._text = set_text
        self._main_lbl.config(text=self._text)

    def configure_lbl(self, font_style=None, label_font_size=None, bg=None, fg=None, anchor=None):
        if font_style is None:
            font_style = self._font_style
        if label_font_size is None:
            label_font_size = self._font_size
        if bg is None:
            bg = self._bg
        if fg is None:
            fg = self._fg
        # if bd is None:
        #     bd = self._bd
        if anchor is None:
            anchor = self._anchor
        self._label.config(anchor=anchor, bg=bg, fg=fg, font=f"{font_style} {label_font_size}")

    def configure_main_lbl(self, font_style=None, font_size=None, bg=None, fg=None, bd=None, anchor=None):
        if font_style is None:
            font_style = self._font_style
        if font_size is None:
            font_size = self._font_size
        if bg is None:
            bg = self._bg
        if fg is None:
            fg = self._fg
        if bd is None:
            bd = self._bd
        if anchor is None:
            anchor = self._anchor
        self._main_lbl.config(anchor=anchor, bg=bg, fg=fg, font=f"{font_style} {font_size}")
        self._main_lbl.grid(pady=(0, bd), padx=(0, 0))

    def config(self, font_style=None, font_size=None, bg=None, fg=None, bd=None, anchor=None, label_font_size=None):
        if font_style is None:
            font_style = self._font_style
        if font_size is None:
            font_size = self._font_size
        if bg is None:
            bg = self._bg
        if fg is None:
            fg = self._fg
        if bd is None:
            bd = self._bd
        if anchor is None:
            anchor = self._anchor
        self._label.config(anchor=anchor, bg=bg, fg=fg, font=f"{font_style} {label_font_size}")
        self._main_lbl.config(anchor=anchor, bg=bg, fg=fg, font=f"{font_style} {font_size}")
        self._main_lbl.grid(pady=(0, bd), padx=(0, 0))


class FrameWithLabel(Frame):
    """
    Example args:
    _frame_with_label_args = {
        'font_style': 'Times',
        'label_font_size': 24,
        'bg': 'white',
        'fg': 'black',
        'bd': 0,
    }
    """
    def __init__(self, root, lbl_text,
                 font_style="Times",
                 label_font_size=24,
                 bg="white",
                 fg="black",
                 bd=0):
        super().__init__(root)
        self.config(bg=fg)

        class _Rows:
            LABEL = 0
            FRAME = 1
        self.grid_rowconfigure(_Rows.LABEL, weight=0)
        self.grid_rowconfigure(_Rows.FRAME, weight=1)

        class _Columns:
            MAIN = 0
        self.grid_columnconfigure(_Columns.MAIN, weight=1)
        self._label = Label(self, text=lbl_text, anchor=W, bg=bg, fg=fg, font=f"{font_style} {label_font_size}")
        self._label.grid(row=_Rows.LABEL, column=_Columns.MAIN, sticky='sew', pady=(0, 0), padx=(0, 0))
        self.frame = Frame(self, bg=bg)
        self.frame.grid(row=_Rows.FRAME, column=_Columns.MAIN, sticky='nsew', pady=(0, bd), padx=(0, 0))


if __name__ == '__main__':
    # WIDGET PLUS
    #   - CheckbuttonPlus
    #   - EntryPlus
    #   - DropdownPlus
    #   - LoggerPlus
    #   - ScrollFramePlus
    # EXTENDED WIDGETS
    #   - ButtonWithBorder
    #   - LabelWithCopy

    # CONFIGURE ROOT CONSTANTS
    _START_HEIGHT = 400
    _START_WIDTH = 400
    _MIN_W_HEIGHT = 300
    _MIN_W_WIDTH = 800

    turquoise = '#59ffc6'
    _MAIN_FG = turquoise
    _MAIN_BG = 'black'

    _root = Tk()
    _root.title("Test")
    _root.config(bg='black')
    # root.minsize(600, 300)
    _root.geometry(f"{_START_WIDTH}x{_START_HEIGHT}")
    # _root.wm_minsize(_MIN_W_WIDTH, _MIN_W_HEIGHT)

    _root.grid_columnconfigure(0, weight=1)
    _root.grid_rowconfigure(0, weight=1)

    _entry_with_label_args = {
        'font_style': 'Times',
        'font_size': 24,
        'bg': _MAIN_BG,
        'fg': _MAIN_FG,
        'bd': 4,
        'label_font_size': 12,
    }
    _dropdown_with_label_args = {
        'font_style': 'Times',
        'font_size': 24,
        'bg': _MAIN_BG,
        'fg': _MAIN_FG,
        'bd': 4,
        'label_font_size': 12,
    }
    _frame_with_label_args = {
        'font_style': 'Times',
        'label_font_size': 24,
        'bg': _MAIN_BG,
        'fg': _MAIN_FG,
        'bd': 0,
    }
    _label_with_label_args = {
        'font_style': 'Times',
        'font_size': 24,
        'bg': _MAIN_BG,
        'fg': _MAIN_FG,
        'bd': 1,
        'label_font_size': 12,
    }
    _frame_with_label = FrameWithLabel(_root, "Test Frame With Label")#, **_frame_with_label_args)  # bd=5, font_style='Helvetica', label_font_size=24, bg=_MAIN_BG, fg=_MAIN_FG)
    _frame_with_label.grid(row=0, column=0, sticky='nsew', pady=(0, 20), padx=(20, 20))
    _frame_with_label.frame.grid_rowconfigure(0, weight=1)
    _frame_with_label.frame.grid_rowconfigure(1, weight=1)
    _frame_with_label.frame.grid_columnconfigure(0, weight=1)

    _entry_with_label = EntryWithLabel(_frame_with_label.frame, "Test Label", **_entry_with_label_args)
    _entry_with_label.grid(row=0, column=0, sticky='ew', pady=(0, 0), padx=20)

    options_list = ['1', '2', '3']
    _dropdown_with_label = DropdownWithLabel(_frame_with_label.frame, "Test Dropdown", options_list=options_list, **_dropdown_with_label_args)
    _dropdown_with_label.grid(row=1, column=0, sticky='ew', pady=(20, 0), padx=(0, 0))

    _label_with_label = LabelWithLabel(_frame_with_label.frame, "Test", "Test Label With Label", **_label_with_label_args)
    _label_with_label.grid(row=2, column=0, sticky='ew', pady=(20, 0), padx=(0, 0))

    _root.mainloop()
#
