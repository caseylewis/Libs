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


class _TestCheckbuttonPlus(Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        # self.config(bg='#202124')

        class _Rows:
            TITLE = 0
            CHECK = 1
            LOG = 2
        self.grid_rowconfigure(
            _Rows.TITLE,
            weight=0,
            minsize=10,
        )
        self.grid_rowconfigure(
            _Rows.CHECK,
            weight=0,
            minsize=10,
        )
        self.grid_rowconfigure(
            _Rows.LOG,
            weight=1,
            minsize=10,
        )

        class _Columns:
            LEFT = 0
            RIGHT = 1
        self.grid_columnconfigure(
            _Columns.LEFT,
            weight=1,
            minsize=100,
        )
        self.grid_columnconfigure(
            _Columns.RIGHT,
            weight=0,
            minsize=10,
        )

        # pad_args = {
        #     'pady': 5,
        #     'padx': 5,
        # }
        # TITLE
        self._title = Label(
            self,
            text="Test Checkbutton Plus",
            **_title_args,
        )
        self._title.grid(
            row=_Rows.TITLE,
            column=_Columns.LEFT,
            columnspan=2,
            **_grid_args,
        )

        # CHECKBUTTON PLUS
        self._check = CheckbuttonPlus(self, height=1)
        self._check.grid(
            row=_Rows.CHECK,
            column=_Columns.LEFT,
            **_grid_args,
        )

        # PRINT BUTTON
        self._print_btn = ButtonWithBorder(
            self,
            text="Print",
            command=lambda: self.__on_print_btn_clicked(),
        )
        self._print_btn.grid(
            row=_Rows.CHECK,
            column=_Columns.RIGHT,
            **_grid_args,
        )

        # LOGGER
        self._logger = TextPlus(self, read_only=True)
        self._logger.grid(
            row=_Rows.LOG,
            column=_Columns.LEFT,
            **_grid_args,
        )

        # CLEAR BUTTON
        self._clear_btn = ButtonWithBorder(
            self,
            text="Clear",
            command=lambda: self.__on_clear_btn_clicked(),
        )
        self._clear_btn.grid(
            row=_Rows.LOG,
            column=_Columns.RIGHT,
            **_grid_args,
        )

    def __on_print_btn_clicked(self):
        val = self._check.get()
        self._logger.append(val)

    def __on_clear_btn_clicked(self):
        self._logger.clear()


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


class _TestEntryPlus(Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        class _Rows:
            TITLE = 0
            ENTRY = 1
            CLEAR = 2
            DEFAULT = 3
            INPUT = 4
            OUTPUT = 5
        self.grid_rowconfigure(
            _Rows.ENTRY,
            weight=0,
            minsize=10,
        )
        self.grid_rowconfigure(
            _Rows.CLEAR,
            weight=0,
            minsize=10,
        )
        self.grid_rowconfigure(
            _Rows.DEFAULT,
            weight=0,
            minsize=10,
        )
        self.grid_rowconfigure(
            _Rows.INPUT,
            weight=0,
            minsize=10,
        )
        self.grid_rowconfigure(
            _Rows.OUTPUT,
            weight=0,
            minsize=10,
        )

        class _Columns:
            ENTRY = 0
            BUTTONS = 1
        self.grid_columnconfigure(
            _Columns.ENTRY,
            weight=1,
            minsize=100,
        )
        self.grid_columnconfigure(
            _Columns.BUTTONS,
            weight=0,
            minsize=10,
        )
        # TITLE
        self._title = Label(
            self,
            text="Test Entry Plus",
            **_title_args
        )
        self._title.grid(
            row=_Rows.TITLE,
            column=_Columns.ENTRY,
            columnspan=2,
            sticky='ew'
        )

        # MAIN ENTRY
        self._entry_plus = EntryPlus(self, default_text="default")
        self._entry_plus.grid(
            row=_Rows.ENTRY,
            column=_Columns.ENTRY,
            **_grid_args,
        )
        # PRINT BUTTON
        self._print_btn = ButtonWithBorder(
            self,
            text="Print",
            command=lambda: self.__on_print_btn_clicked()
        )
        self._print_btn.grid(
            row=_Rows.ENTRY,
            column=_Columns.BUTTONS,
            **_grid_args,
        )
        # CLEAR ENTRY BUTTON
        self._clear_entry_btn = ButtonWithBorder(
            self,
            text="Clear",
            command=lambda: self.__on_clear_entry_btn_clicked()
        )
        self._clear_entry_btn.grid(
            row=_Rows.CLEAR,
            column=_Columns.BUTTONS,
            **_grid_args,
        )
        # DEFAULT BUTTON
        self._default_btn = ButtonWithBorder(
            self,
            text="Default",
            command=lambda: self.__on_default_btn_clicked()
        )
        self._default_btn.grid(
            row=_Rows.DEFAULT,
            column=_Columns.BUTTONS,
            **_grid_args,
        )
        # INPUT ENTRY
        self._input_entry_plus = EntryPlus(self)
        self._input_entry_plus.grid(
            row=_Rows.INPUT,
            column=_Columns.ENTRY,
            **_grid_args,
        )
        # SET BUTTON
        self._set_btn = ButtonWithBorder(
            self,
            text="Set",
            command=lambda: self.__on_set_btn_clicked()
        )
        self._set_btn.grid(
            row=_Rows.INPUT,
            column=_Columns.BUTTONS,
            **_grid_args,
        )

        # OUTPUT ENTRY
        self._output_entry_plus = TextPlus(self, read_only=True, height=1)
        self._output_entry_plus.grid(
            row=_Rows.OUTPUT,
            column=_Columns.ENTRY,
            **_grid_args,
        )

        # CLEAR OUTPUT BUTTON
        self._clear_output_btn = ButtonWithBorder(
            self,
            text="Clear",
            command=lambda: self.__on_clear_output_btn_clicked()
        )
        self._clear_output_btn.grid(
            row=_Rows.OUTPUT,
            column=_Columns.BUTTONS,
            **_grid_args,
        )

    def __on_print_btn_clicked(self):
        text = self._entry_plus.get()
        self._output_entry_plus.set(text)

    def __on_clear_entry_btn_clicked(self):
        self._entry_plus.clear()

    def __on_default_btn_clicked(self):
        self._entry_plus.default()

    def __on_set_btn_clicked(self):
        text = self._input_entry_plus.get()
        self._entry_plus.set(text)

    def __on_clear_output_btn_clicked(self):
        self._output_entry_plus.clear()


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


class _TestDropdownPlus(Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        class Rows:
            TITLE = 0
            TOP = 1
            BOTTOM = 2
        self.grid_rowconfigure(
            Rows.TOP,
            weight=0,
            minsize=10,
            uniform='rows',
        )
        self.grid_rowconfigure(
            Rows.BOTTOM,
            weight=0,
            minsize=10,
            uniform='rows',
        )

        class Columns:
            LEFT = 0
            RIGHT = 1
        self.grid_columnconfigure(
            Columns.LEFT,
            weight=5,
            minsize=50,
            # uniform=
        )
        self.grid_columnconfigure(
            Columns.RIGHT,
            weight=0,
            minsize=5,
            # uniform=
        )
        # TITLE LABEL
        self._title = Label(
            self,
            text="Test Dropdown Plus",
            **_title_args,
        )
        self._title.grid(
            row=Rows.TITLE,
            column=Columns.LEFT,
            columnspan=2,
            sticky='nsew',
        )

        # ENTRY
        self._entry = EntryPlus(self)
        self._entry.grid(
            row=Rows.TOP,
            column=Columns.LEFT,
            sticky='nsew',
        )
        # DROPDOWN
        self._dropdown = DropdownPlus(self, ['1', '2', '3'])
        self._dropdown.grid(
            row=Rows.BOTTOM,
            column=Columns.LEFT,
            sticky='nsew',
        )
        # PLUS BUTTON
        self._plus = ButtonWithBorder(self, text='[+]', command=lambda: self.__on_plus_clicked())
        self._plus.grid(
            row=Rows.TOP,
            column=Columns.RIGHT,
            sticky='nsew',
        )
        # MINUS BUTTON
        self._minus = ButtonWithBorder(self, text='[-]', command=lambda: self.__on_minus_clicked())
        self._minus.grid(
            row=Rows.BOTTOM,
            column=Columns.RIGHT,
            sticky='nsew',
        )

    def __on_plus_clicked(self):
        entry_text = self._entry.get()
        if entry_text is not '':
            self._dropdown.add_option(entry_text)

    def __on_minus_clicked(self):
        current_option = self._dropdown.get()
        self._dropdown.remove_option(current_option)


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


class _TestScrollframePlus(Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        class _Rows:
            TITLE = 0
            SCROLLFRAME = 1
            BUTTONS = 2
        self.grid_rowconfigure(
            _Rows.TITLE,
            weight=0,
            minsize=10,
        )
        self.grid_rowconfigure(
            _Rows.SCROLLFRAME,
            weight=1,
            minsize=100,
        )
        self.grid_rowconfigure(
            _Rows.BUTTONS,
            weight=0,
            minsize=10,
        )

        class _Columns:
            MAIN = 0
        self.grid_columnconfigure(
            _Columns.MAIN,
            weight=1,
            minsize=100,
        )
        # TITLE
        self._title = Label(
            self,
            text="Test ScrollFrame Plus",
            **_title_args,
        )
        self._title.grid(
            row=_Rows.TITLE,
            column=_Columns.MAIN,
            sticky='ew',

        )
        # SCROLLFRAME PLUS
        # TOGGLE BUTTON


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

    _root = Tk()
    _root.config(bg='#59ffc6')
    # root.minsize(600, 300)
    _root.geometry(f"{_START_WIDTH}x{_START_HEIGHT}")
    _root.wm_minsize(_MIN_W_WIDTH, _MIN_W_HEIGHT)

    # CONFIGURE COLUMNS
    class _Columns:
        DESC = 0
        TEST = 1
    uniform_minsize = 200
    buffer_minsize = 50
    _root.grid_columnconfigure(
        _Columns.DESC,
        weight=1,
        minsize=uniform_minsize,
        uniform='desc'
    )
    _root.grid_columnconfigure(
        _Columns.TEST,
        weight=5,
        minsize=uniform_minsize,
        uniform='test'
    )

    # CONFIGURE ROWS
    class _Rows:
        CHECK = 0
        ENTRY = 1
        # TEXT = 2
        DROPDOWN = 3
    _root.grid_rowconfigure(
        _Rows.CHECK,
        weight=1,
        minsize=10,
        uniform='uniform_rows'
    )
    _root.grid_rowconfigure(
        _Rows.ENTRY,
        weight=1,
        minsize=300,
        # uniform='uniform_rows'
    )
    _root.grid_rowconfigure(
        _Rows.DROPDOWN,
        weight=1,
        minsize=10,
        uniform='uniform_rows'
    )
    # LOCAL STYLE ARGS
    _text_args = {
        'width': 50,
        'height': 1,
        'read_only': True,
    }
    _test_frame_args = {
        'bg': '#59ffc6',
    }
    # LOCAL GRID ARGS
    _text_grid_args = {
        'pady': _grid_args['pady'],
        'padx': _grid_args['padx'],
        'sticky': 'nsew',
    }
    _test_grid_args = {
        'pady': _grid_args['pady'],
        'padx': _grid_args['padx'],
        'sticky': 'nsew',
    }

########################################################################################################################
    # TEXT CHECKBUTTON PLUS
    text_checkbutton_plus = TextPlus(
        _root,
        **_text_args,
    )
    text_checkbutton_plus.set(
        "This is to test the CheckbuttonPlus class."
        "\n\n"
        "Test new line."
    )
    text_checkbutton_plus.grid(
        row=_Rows.CHECK,
        column=_Columns.DESC,
        **_text_grid_args,
    )

    # TEST CHECKBUTTON PLUS
    test_checkbutton_plus = _TestCheckbuttonPlus(_root, **_test_frame_args)
    test_checkbutton_plus.grid(
        row=_Rows.CHECK,
        column=_Columns.TEST,
        **_test_grid_args,
    )

########################################################################################################################
    # TEXT ENTRY PLUS
    text_entry_plus = TextPlus(
        _root,
        **_text_args,
    )
    text_entry_plus.set(
        "This is to test the EntryPlus class."
        "\n\n"
        "Print: Prints what is currently in the Main Entry to the Output Entry (bottom)."
        "\n\n"
        "Clear: Clears the Main Entry."
    )
    text_entry_plus.grid(
        row=_Rows.ENTRY,
        column=_Columns.DESC,
        **_text_grid_args,
    )

    # TEST ENTRY PLUS
    test_entry_plus = _TestEntryPlus(
        _root,
        **_test_frame_args,
    )
    test_entry_plus.grid(
        row=_Rows.ENTRY,
        column=_Columns.TEST,
        **_test_grid_args,
    )

########################################################################################################################
    # TEXT DROPDOWN PLUS
    text_dropdown_plus = TextPlus(
        _root,
        **_text_args,
    )
    text_dropdown_plus.grid(
        row=_Rows.DROPDOWN,
        column=_Columns.DESC,
        **_text_grid_args,
    )
    # TEST DROPDOWN PLUS
    test_dropdown_plus = _TestDropdownPlus(
        _root,
        **_test_frame_args,
    )
    test_dropdown_plus.grid(
        row=_Rows.DROPDOWN,
        column=_Columns.TEST,
        **_test_grid_args,
    )

    _root.update()

    _root.mainloop()
