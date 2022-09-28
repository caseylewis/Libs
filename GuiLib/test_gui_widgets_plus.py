try:
    from Libs.GuiLib.gui_widgets_plus import *
except Exception as e:
    from GuiLib.gui_widgets_plus import *


########################################################################################################################
# LOCAL STYLE DEFINITION
MAIN_BG = '#59ffc6'
_title_args = {
    'bg': 'black',
    'fg': 'white',
    'font': ("Helvetica", 18)
}
########################################################################################################################
# LOCAL GRID DEFINITION
_grid_args = {
    'pady': 5,
    'padx': 20,
    'sticky': 'new',
}
########################################################################################################################


class _TestCheckbuttonPlus(Frame):
    """
    Tests the CheckbuttonPlus widget and all it's functionality.
    Methods tested:
    -
    """
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        # self.config(bg='#202124')

        class _Rows:
            TITLE = 0
            CHECK = 1
            LOG = 2
        self.grid_rowconfigure(_Rows.TITLE, weight=0, minsize=10)
        self.grid_rowconfigure(_Rows.CHECK, weight=0, minsize=10)
        self.grid_rowconfigure(_Rows.LOG, weight=1, minsize=10)

        class _Columns:
            LEFT = 0
            RIGHT = 1
        self.grid_columnconfigure(_Columns.LEFT, weight=1, minsize=100)
        self.grid_columnconfigure(_Columns.RIGHT, weight=0, minsize=10)

        # pad_args = {
        #     'pady': 5,
        #     'padx': 5,
        # }
        # TITLE
        self._title = Label(self, text="Test Checkbutton Plus", **_title_args)
        self._title.grid(row=_Rows.TITLE, column=_Columns.LEFT, columnspan=2, **_grid_args)
        # CHECKBUTTON PLUS
        self._check = CheckbuttonPlus(self, height=1)
        self._check.grid(row=_Rows.CHECK, column=_Columns.LEFT, **_grid_args)

        _btn_border_args = {
            'bg': self['bg'],
            'fg': 'black',
        }
        # PRINT BUTTON
        self._print_btn = ButtonWithBorder(self, text="Print", command=lambda: self.__on_print_btn_clicked(), **_btn_border_args)
        self._print_btn.grid(row=_Rows.CHECK, column=_Columns.RIGHT, **_grid_args)
        # LOGGER
        self._logger = TextPlus(self, read_only=True, height=2)
        self._logger.grid(row=_Rows.LOG, column=_Columns.LEFT, **_grid_args)
        # CLEAR BUTTON
        self._clear_btn = ButtonWithBorder(self, text="Clear", command=lambda: self.__on_clear_btn_clicked(), **_btn_border_args)
        self._clear_btn.grid(row=_Rows.LOG, column=_Columns.RIGHT, **_grid_args)

    def __on_print_btn_clicked(self):
        val = self._check.get()
        self._logger.append(val)

    def __on_clear_btn_clicked(self):
        self._logger.clear()


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
        self.grid_rowconfigure(_Rows.ENTRY, weight=0, minsize=10)
        self.grid_rowconfigure(_Rows.CLEAR, weight=0, minsize=10)
        self.grid_rowconfigure(_Rows.DEFAULT, weight=0, minsize=10)
        self.grid_rowconfigure(_Rows.INPUT, weight=0, minsize=10)
        self.grid_rowconfigure(_Rows.OUTPUT, weight=0, minsize=10)

        class _Columns:
            ENTRY = 0
            BUTTONS = 1
        self.grid_columnconfigure(_Columns.ENTRY, weight=1, minsize=100)
        self.grid_columnconfigure(_Columns.BUTTONS, weight=0, minsize=10)

        # STYLES
        _btn_border_args = {
            'bg': self['bg'],
            'fg': 'black',
        }
        # TITLE
        self._title = Label(self, text="Test Entry Plus", **_title_args)
        self._title.grid(row=_Rows.TITLE, column=_Columns.ENTRY, columnspan=2, sticky='ew')
        # MAIN ENTRY
        self._entry_plus = EntryPlus(self, default_text="default")
        self._entry_plus.grid(row=_Rows.ENTRY, column=_Columns.ENTRY, **_grid_args)
        # PRINT BUTTON
        self._print_btn = ButtonWithBorder(self, text="Print", command=lambda: self.__on_print_btn_clicked(), **_btn_border_args)
        self._print_btn.grid(row=_Rows.ENTRY, column=_Columns.BUTTONS, **_grid_args)
        # CLEAR ENTRY BUTTON
        self._clear_entry_btn = ButtonWithBorder(self, text="Clear", command=lambda: self.__on_clear_entry_btn_clicked(), **_btn_border_args)
        self._clear_entry_btn.grid(row=_Rows.CLEAR, column=_Columns.BUTTONS, **_grid_args)
        # DEFAULT BUTTON
        self._default_btn = ButtonWithBorder(self, text="Default", command=lambda: self.__on_default_btn_clicked(), **_btn_border_args)
        self._default_btn.grid(row=_Rows.DEFAULT, column=_Columns.BUTTONS, **_grid_args)
        # INPUT ENTRY
        self._input_entry_plus = EntryPlus(self)
        self._input_entry_plus.grid(row=_Rows.INPUT, column=_Columns.ENTRY, **_grid_args)
        # SET BUTTON
        self._set_btn = ButtonWithBorder(self, text="Set", command=lambda: self.__on_set_btn_clicked(), **_btn_border_args)
        self._set_btn.grid(row=_Rows.INPUT, column=_Columns.BUTTONS, **_grid_args)
        # OUTPUT ENTRY
        self._output_entry_plus = TextPlus(self, read_only=True, height=1)
        self._output_entry_plus.grid(row=_Rows.OUTPUT, column=_Columns.ENTRY, **_grid_args)
        # CLEAR OUTPUT BUTTON
        self._clear_output_btn = ButtonWithBorder(self, text="Clear", command=lambda: self.__on_clear_output_btn_clicked(), **_btn_border_args)
        self._clear_output_btn.grid(row=_Rows.OUTPUT, column=_Columns.BUTTONS, **_grid_args)

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


class _TestDropdownPlus(Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        class Rows:
            TITLE = 0
            TOP = 1
            BOTTOM = 2
        self.grid_rowconfigure(Rows.TOP, weight=0, minsize=10, uniform='rows')
        self.grid_rowconfigure(Rows.BOTTOM, weight=0, minsize=10, uniform='rows')

        class Columns:
            LEFT = 0
            RIGHT = 1
        self.grid_columnconfigure(Columns.LEFT, weight=5, minsize=50)
        self.grid_columnconfigure(Columns.RIGHT, weight=0, minsize=5)

        # STYLES
        _btn_border_args = {
            'bg': self['bg'],
            'fg': 'black',
        }
        # TITLE LABEL
        self._title = Label(self, text="Test Dropdown Plus", **_title_args)
        self._title.grid(row=Rows.TITLE, column=Columns.LEFT, columnspan=2, sticky='nsew')
        # ENTRY
        self._entry = EntryPlus(self)
        self._entry.grid(row=Rows.TOP, column=Columns.LEFT, sticky='nsew')
        # DROPDOWN
        self._dropdown = DropdownPlus(self, ['1', '2', '3'])
        self._dropdown.grid(row=Rows.BOTTOM, column=Columns.LEFT, sticky='nsew')
        # PLUS BUTTON
        self._plus = ButtonWithBorder(self, text='[+]', command=lambda: self.__on_plus_clicked(), **_btn_border_args)
        self._plus.grid(row=Rows.TOP, column=Columns.RIGHT, sticky='nsew')
        # MINUS BUTTON
        self._minus = ButtonWithBorder(self, text='[-]', command=lambda: self.__on_minus_clicked(), **_btn_border_args)
        self._minus.grid(row=Rows.BOTTOM, column=Columns.RIGHT, sticky='nsew')

    def __on_plus_clicked(self):
        entry_text = self._entry.get()
        if entry_text is not '':
            self._dropdown.add_option(entry_text)

    def __on_minus_clicked(self):
        current_option = self._dropdown.get()
        self._dropdown.remove_option(current_option)


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
    _START_WIDTH = 800
    _MIN_W_HEIGHT = 300
    _MIN_W_WIDTH = 800

    # CREATE ROOT WINDOW
    _root = Tk()
    _root.config(bg=MAIN_BG)
    _root.title("Test Gui Widgets Plus")
    # root.minsize(600, 300)
    _root.geometry(f"{_START_WIDTH}x{_START_HEIGHT}")
    # _root.wm_minsize(_MIN_W_WIDTH, _MIN_W_HEIGHT)

    _root.grid_columnconfigure(0, weight=1, minsize=500)
    _root.grid_rowconfigure(0, weight=1, minsize=50)

    # CREATE MAIN SCROLL FRAME
    _main_scroll_frame = ScrollFramePlus(_root, bg=MAIN_BG)
    _main_scroll_frame.grid(row=0, column=0, sticky='nsew', pady=5, padx=5)

    # CONFIGURE COLUMNS
    class _Columns:
        DESC = 0
        TEST = 1
    uniform_minsize = 150
    buffer_minsize = 50
    _main_scroll_frame.view_port.grid_columnconfigure(_Columns.DESC, weight=1, minsize=uniform_minsize, uniform='desc')
    _main_scroll_frame.view_port.grid_columnconfigure(_Columns.TEST, weight=5, minsize=uniform_minsize, uniform='test')

    # CONFIGURE ROWS
    class _Rows:
        CHECK = 0
        ENTRY = 1
        # TEXT = 2
        DROPDOWN = 3
    _main_scroll_frame.view_port.grid_rowconfigure(_Rows.CHECK, weight=1, minsize=10)
    _main_scroll_frame.view_port.grid_rowconfigure(_Rows.ENTRY, weight=1, minsize=300)
    _main_scroll_frame.view_port.grid_rowconfigure(_Rows.DROPDOWN, weight=1, minsize=10)
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
    text_checkbutton_plus = TextPlus(_main_scroll_frame.view_port, **_text_args)
    text_checkbutton_plus.grid(row=_Rows.CHECK, column=_Columns.DESC, **_text_grid_args)
    text_checkbutton_plus.set(
        "This is to test the CheckbuttonPlus class."
        "\n\n"
        "Test new line."
    )

    # TEST CHECKBUTTON PLUS
    test_checkbutton_plus = _TestCheckbuttonPlus(_main_scroll_frame.view_port, **_test_frame_args)
    test_checkbutton_plus.grid(row=_Rows.CHECK, column=_Columns.TEST, **_test_grid_args)

########################################################################################################################
    # TEXT ENTRY PLUS
    text_entry_plus = TextPlus(_main_scroll_frame.view_port, **_text_args)
    text_entry_plus.grid(row=_Rows.ENTRY, column=_Columns.DESC, **_text_grid_args)
    text_entry_plus.set(
        "This is to test the EntryPlus class."
        "\n\n"
        "Print: Prints what is currently in the Main Entry to the Output Entry (bottom)."
        "\n\n"
        "Clear: Clears the Main Entry."
    )

    # TEST ENTRY PLUS
    test_entry_plus = _TestEntryPlus(_main_scroll_frame.view_port, **_test_frame_args)
    test_entry_plus.grid(row=_Rows.ENTRY, column=_Columns.TEST, **_test_grid_args)

########################################################################################################################
    # TEXT DROPDOWN PLUS
    text_dropdown_plus = TextPlus(_main_scroll_frame.view_port, **_text_args)
    text_dropdown_plus.grid(row=_Rows.DROPDOWN, column=_Columns.DESC, **_text_grid_args)
    text_dropdown_plus.set(
        "This is to test the Dropdown Plus class."
    )
    # TEST DROPDOWN PLUS
    test_dropdown_plus = _TestDropdownPlus(_main_scroll_frame.view_port, **_test_frame_args)
    test_dropdown_plus.grid(row=_Rows.DROPDOWN, column=_Columns.TEST, **_test_grid_args)

    _root.update()

    _root.mainloop()
