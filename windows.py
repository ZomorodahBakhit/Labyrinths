import curses
import time
import curses.textpad
from input_handler import InputHandler


class Windows:

    def __init__(self, stdscr: curses.window, input_handler: InputHandler):
        """
        Initialize the Windows class.

        :param stdscr: is the main window object from curses.
        :param input_handler: is an instance of the InputHandler class for handling user input.
        """
        self.stdscr = stdscr
        self.input_handler = input_handler
        self.stdscrheight, self.stdscrwidth = self.stdscr.getmaxyx()  # Get dimensions of the main screen
        self.middle_height = self.stdscrheight // 2  # Calculate the middle height of the screen
        self.middle_width = self.stdscrwidth // 2  # Calculate the middle width of the screen

    def handle_input(self):
        """
        Handle user input by delegating to the InputHandler instance.
        """
        return self.input_handler.handle_input(self)

    def clear_and_refresh(self, window=None):
        """
        Clear and refresh the given window, or the main window if no window is specified.

        :param window: is an optional specific curses window to clear and refresh.
        """
        if window is None:
            self.stdscr.clear()
            self.stdscr.refresh()
        else:
            window.clear()
            window.refresh()

    @staticmethod
    def type_text(window: curses.window, text, start_y, start_x, delay=0.09):
        """
        Simulate typing text in the given window with a delay between each character.

        :param window: is the curses window object to print the text in.
        :param text: is the text to be typed.
        :param start_y: is the starting y position in the window.
        :param start_x: is the starting x position in the window.
        :param delay: is the delay (in seconds) between each character.
        """
        y, x = start_y, start_x  # Initialize current position
        
        for char in text:
            if char == '\n':  # Move to next line when encountering a newline character
                y += 1
                x = start_x  # Reset x position to the starting x
            else:
                window.addch(y, x, char)
                x += 1  # Move to the next character position horizontally
            
            window.refresh()
            time.sleep(delay)


class Menu_Window(Windows):
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensure that only one instance of Menu_Window is created (Singleton pattern).
        """
        if cls._instance is None:
            cls._instance = super(Menu_Window, cls).__new__(cls)
        return cls._instance

    def __init__(self, stdscr: curses.window, input_handler: InputHandler):
        """
        Initialize the Menu_Window class.

        :param stdscr: is the main window object from curses.
        :param input_handler: is an instance of the InputHandler class for handling user input.
        """
        if not hasattr(self, '_initialized'):
            super().__init__(stdscr, input_handler)
            self._initialized = True

            # Menu options
            self.menu = ["Continue", "New Game", "Settings", "Quit"]
            self.selected_row_index = 0  # This is the index of the currently selected menu option

            # ASCII art for open and closed scrolls
            self.open_scroll = [
                " | |   __ _| |__ _  _ _ _(_)_ _| |_| |_  ___",
                " | |__/ _` | '_ \ || | '_| | ' \  _| ' \(_-<",
                " |____\__,_|_.__/\_, |_| |_|_||_\__|_||_/__/",
                "                 |__/                       ",
                "         __________________________         ",
                "       =(__    ___      __        _)=       ",
                "         |                        |         ",
                "         |                        |         ",
                "         |                        |         ",
                "         |                        |         ",
                "         |                        |         ",
                "         |                        |         ",
                "         |                        |         ",
                "         |                        |         ",
                "         |__    _ __   __    _ ___|         ",
                "       =(______________________ ___)=       ",
            ]

            self.closed_scroll = [
                " | |   __ _| |__ _  _ _ _(_)_ _| |_| |_  ___",
                " | |__/ _` | '_ \ || | '_| | ' \  _| ' \(_-<",
                " |____\__,_|_.__/\_, |_| |_|_||_\__|_||_/__/",
                "                 |__/                       ",    
                "         __________________________         ",
                "       =(__    ___      __        _)=       ",
                "         |                        |         ",
                "       =(__________________________)=       ",
            ]

    def render_closed_scroll(self):
        """
        Render the closed scroll ASCII art in the center of the screen.
        """
        for index, row in enumerate(self.closed_scroll):
            x = self.middle_width - len(row) // 2  # Center the text horizontally
            y = self.middle_height - len(self.closed_scroll) // 2 + index  # Center the text vertically
            self.stdscr.addstr(y, x, row)

    def render_open_scroll(self):
        """
        Render the open scroll ASCII art in the center of the screen.
        """
        for index, row in enumerate(self.open_scroll):
            x = self.middle_width - len(row) // 2  # Center the text horizontally
            y = self.middle_height - len(self.open_scroll) // 2 + index  # Center the text vertically
            self.stdscr.addstr(y, x, row)

    def render_menu(self):
        """
        Render the menu options in the center of the screen, highlighting the selected option.
        """
        for index, row in enumerate(self.menu):
            x = self.middle_width - len(row) // 2  # Center the text horizontally
            y = self.middle_height - len(self.menu) // 2 + index + 2  # Center the text vertically with offset for game title

            if index == self.selected_row_index:
                self.stdscr.addstr(y, x, "> " + row)  # Highlight the selected menu option
            else:
                self.stdscr.addstr(y, x, row)

    def render(self):
        """
        Clear the screen and render the closed scroll, open scroll, and menu.
        """
        self.clear_and_refresh()

        self.render_closed_scroll()
        self.stdscr.refresh()
        time.sleep(0.2)  # Pause for 0.2 seconds to show the closed scroll
        self.stdscr.clear()
        self.render_open_scroll()
        self.render_menu()
        self.stdscr.refresh()
