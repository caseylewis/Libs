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


class CheckbuttonPlus(Checkbutton):
    ON = 1
    OFF = 0

    def __init__(self, root, select_func=None, deselect_func=None, *args, **kwargs):
        self._select_func = select_func
        self._deselect_func = deselect_func
        self._var = IntVar()
        self._var.trace('w', lambda x, y, z: self.__on_val_change())
        super().__init__(root, variable=self._var, *args, **kwargs)

    def get(self):
        return self._var.get()

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

    def default(self):
        self.set(self._default_text)

    def clear(self):
        self.delete(0, END)

    def set(self, set_text):
        self.clear()
        self.insert(0, set_text)


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

        self.config(**kwargs)

    def __on_change_callback(self):
        if self.on_change_func is not None:
            self.on_change_func()

    def add_option(self, option):
        self._options_list.append(option)
        menu = self["menu"]
        menu.delete(0, "end")
        for string in self._options_list:
            menu.add_command(label=string, command=lambda value=string: self._var.set(value))

    def remove_option(self, option_string):
        for option in self._options_list:
            if option_string == option:
                self._options_list.remove(option)

        menu = self["menu"]
        menu.delete(0, "end")
        for string in self._options_list:
            menu.add_command(label=string, command=lambda value=string: self._var.set(value))
        self.default()

    def set_options(self, options_list):
        self._options_list = options_list

        menu = self["menu"]
        menu.delete(0, "end")
        for string in self._options_list:
            menu.add_command(label=string, command=lambda value=string: self._var.set(value))
        self.default()

    def default(self):
        self._var.set(self._options_list[0])

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
        'bg': 'white',
        'fg': '#ff4d5b', # LIGHTRED
        'bd': 3
    }
    """
    def __init__(self, root, btn_text, command,
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
        self._btn = Button(self, text=btn_text.upper(), command=self.__command, font=font, bg=self.bg, fg=self.fg, relief='flat')
        self._btn.grid(row=0, column=0, sticky='nsew', pady=self.bd, padx=self.bd)


class LabelWithCopy(Frame):
    """
    Example args:
    bordered_button_args = {
        'font_style': 'Times',
        'font_size': 18,
        'font_extras': 'italic',
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

    root = Tk()
    root.config(bg='yellow')
    # root.minsize(600, 300)
    START_HEIGHT = 400
    START_WIDTH = 400
    root.geometry(f"{START_WIDTH}x{START_HEIGHT}")
    MIN_W_HEIGHT = 300
    MIN_W_WIDTH = 800
    root.wm_minsize(MIN_W_WIDTH, MIN_W_HEIGHT)

    class Columns:
        FIRST = 0
        BUFFER_1 = 1
        SECOND = 2
        THIRD = 3
        BUFFER_2 = 4


    class Rows:
        TOP = 0
        MIDDLE = 1
        BOTTOM = 2


    # CONFIGURE COLUMNS
    uniform_minsize = 200
    buffer_minsize = 50
    root.grid_columnconfigure(
        Columns.FIRST,
        weight=0,
        minsize=100,
        uniform='first'
    )
    root.grid_columnconfigure(
        Columns.BUFFER_1,
        weight=1,
        minsize=buffer_minsize,
        uniform='buffer'
    )
    root.grid_columnconfigure(
        Columns.SECOND,
        weight=1,
        minsize=uniform_minsize,
        uniform='uniform_columns'
    )
    root.grid_columnconfigure(
        Columns.THIRD,
        weight=1,
        minsize=uniform_minsize,
        uniform='uniform_columns'
    )
    root.grid_columnconfigure(
        Columns.BUFFER_2,
        weight=1,
        minsize=buffer_minsize,
        uniform='buffer'
    )
    # CONFIGURE ROWS
    root.grid_rowconfigure(
        Rows.TOP,
        weight=0,
        minsize=10,
        uniform='top'
    )
    root.grid_rowconfigure(
        Rows.MIDDLE,
        weight=1,
        minsize=20,
        uniform='uniform_rows'
    )
    root.grid_rowconfigure(
        Rows.BOTTOM,
        weight=1,
        minsize=20,
        uniform='uniform_rows'
    )

    grid_args = {
        'sticky': 'nsew',
    }

    def get_row_or_column_from_tag(tag_dict, tag):
        """
        Pass in tag
        """
        for row, tag_list in tag_dict.items():
            if tag in tag_list:
                return row
        raise Exception(f"Tag: [{tag}] NOT found in list.")

    # CHECKBUTTONPLUS
    checkbutton_plus = CheckbuttonPlus(root)
    checkbutton_plus.grid(
        row=Rows.TOP,
        column=Columns.FIRST,
        sticky='ew'
    )

    # DROPDOWNPLUS
    dropdown_options = ['one', 'two', 'three']
    dropdown_plus = DropdownPlus(root, dropdown_options)
    dropdown_plus.grid(
        row=Rows.TOP,
        column=Columns.SECOND,
        sticky='nsew'
    )

    # ENTRYPLUS
    entry_plus = EntryPlus(root, default_text='default text')
    entry_plus.grid(
        row=Rows.TOP,
        column=Columns.THIRD,
        sticky='ew'
    )

    # LOGGERPLUS
    logger_plus = LoggerPlus(root, width=5, height=2)
    logger_plus.grid(
        row=Rows.MIDDLE,
        column=Columns.SECOND,
        columnspan=2,
        **grid_args
    )
    logger_plus.log("This is a test of the logger log functionality.")

    # SCROLLFRAMEPLUS
    scrollframe_plus = ScrollFramePlus(root, hide_scrollbar=False)
    scrollframe_plus.grid(row=Rows.BOTTOM, column=Columns.FIRST, **grid_args)
    scrollframe_plus.grid_columnconfigure(0, weight=1)
    scrollframe_plus.config(bg='red', width=200, height=100)
    # VIEW PORT
    scrollframe_plus.view_port.grid(pady=5, padx=5, ipadx=5, ipady=5, sticky='nsew')
    scrollframe_plus.view_port.grid_columnconfigure(0, weight=1)
    scrollframe_plus.view_port.config(bg='orange')
    for button in range(5):
        btn = Button(scrollframe_plus.view_port, text=f"button {button+1}", command=lambda text=f"button {button+1} clicked": print(text))
        btn.grid(row=button, sticky='ew', padx=10)

    root.update()

    root.mainloop()
