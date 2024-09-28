import curses
import time
from windows import Windows
from input_handler import InputHandler
from entity import Entity




##fix
class Narration_Window(Windows):
    def __init__(self, stdscr: curses.window, input_handler: InputHandler, name, height = 5, width = 50, box = True):
        super().__init__(stdscr, input_handler)
        self.height = height
        self.width = width
        self.box = box
        
       
        x = self.middle_width - self.width//2
        y = self.middle_height + (self.height*2) + 5
        self.window = curses.newwin(self.height, self.width, y, x)
        
    

        if name == "":
            name = "Hudson"
        self.name = name.capitalize()
        


    def render_narration(self, narration, delay = 0.03):
        
        if self.box == True:
            self.window.box()
        text = f"{self.name}: {narration}"
        Windows.type_text(self.window, text, 1, 1, delay)

        s = self.handle_input()
        while s != 's':
            s = self.handle_input()
        
        self.clear_and_refresh(self.window)


class Battle_Window(Windows):
    def __init__(self, stdscr: curses.window, input_handler: InputHandler, maze,  view_y, view_x, player_y, player_x, view_height = 18, view_width = 64):

        
        super().__init__(stdscr, input_handler)
        
    
        self.maze = maze 
        self.walls = set()

        self.viewport_start_y = (self.stdscrheight // 2) - (view_height//2)
        self.viewport_start_x = (self.stdscrwidth // 2) - (view_width//2)

        self.view_y, self.view_x = view_y, view_x#0, 85
        self.player_y, self.player_x =player_y, player_x# 4, 150
        self.view_height, self.view_width = view_height +self.viewport_start_y, view_width+self.viewport_start_x  # Size of the visible area

        # Center the viewport on the screen

        # Create the maze pad
        self.box = curses.newwin(view_height + 5, view_width + 10, self.viewport_start_y-2, self.viewport_start_x -5)
        
        self.window = curses.newpad(len(self.maze)*2, len(self.maze[0])*2)
        
        self.entity = Entity(self.window, self.player_y, self.player_x, '@')

        # Populate the maze with walls and paths (simple random generation)
        for y, row in enumerate(self.maze):
            for x, char in enumerate(row):
                self.window.addstr(y, x, char)
                if char != ' ':  # Add all non-space characters as walls
                    self.walls.add((y, x))

        
    
    def get_window_data(self):
        pass
    
    def render(self):
        self.box.box()
        self.box.refresh()
        self.entity.draw()
        self.window.refresh(self.view_y, self.view_x, self.viewport_start_y, self.viewport_start_x,  self.view_height - 1,   self.view_width - 1)

    
       

    def should_exit(self): #(12,1)
        # Define exit condition: player should be in a specific position
      return  (self.entity.position() == (12,1))
        

class DisplayWindow(Windows):
    def __init__(self, stdscr: curses.window, input_handler: InputHandler, height: int, width: int, display: list):
        super().__init__(stdscr, input_handler)
        self.height = height
        self.width = width
        self.display = display

        self.window_y = self.middle_height - self.height // 2
        self.window_x = self.middle_width - self.width // 2
        self.window = curses.newwin(self.height, self.width, self.window_y, self.window_x)
        
        self.walls = set()

    def render(self, Box = True, Walls = True):
        if Box:
            self.window.box()

        for index, row in enumerate(self.display):
            display_x = (self.width - len(row)) // 2
            display_y = self.height // 2 - len(self.display) // 2 + index
            self.window.addstr(display_y, display_x, row)

            if Walls:
                for i, char in enumerate(row):
                    if char != ' ':  # Assuming non-empty characters (excluding borders) should be stored as walls
                        self.walls.add((display_y, display_x + i))

        self.window.refresh()

class ExitWindow(DisplayWindow):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ExitWindow, cls).__new__(cls)
        return cls._instance

    def __init__(self, stdscr: curses.window, input_handler: InputHandler):
        if not hasattr(self, '_initialized'):
            message = [
                "Are you sure you want to quit?",
                "                              ",
                "                              ",
                "       Y[es]       N[o]       ",
                "                              ",
            ]
            super().__init__(stdscr, input_handler, height=10, width=34, display=message)
            self._initialized = True

class NameBox(DisplayWindow):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NameBox, cls).__new__(cls)
        return cls._instance

    def __init__(self, stdscr: curses.window, input_handler: InputHandler):
        if not hasattr(self, '_initialized'):
            self.text_box = None
            message = [
                "  What is your name, player?  ",
                "                              ",
                "                              ",
                "                              ",
                "                              ",
                "                              ",
            ]
            super().__init__(stdscr, input_handler, height=10, width=34, display=message)
            self._initialized = True

    def render(self):
        super().render()
        player_name_window = curses.newwin(1, 6, self.window_y + 6, self.window_x + 14)
        self.text_box = curses.textpad.Textbox(player_name_window)






class House_Window(DisplayWindow):
    def __init__(self, stdscr: curses.window, input_handler: InputHandler, x = 24, y = 4):
        house = [
            "+------------------------------+",
            "|  |        (o)|    {_____ _}  |",
            "|  |_/_[-|-]___|   |_| ____|_| |",
            "|                  | |     | | |",
            "|     [___]        | |     | | |",
            "|                  | |     | | |",
            "|                  | |     | | |",  # Bed at the top-left
            "|                  |_|_____|_| |",
            "| ____                         |",
            "||____|                        |",  # Desk in the bottom-left
            "||____/                        |",
            "|                              |",
            "|                              |",
            "+_____###_____    _____###_____+",
            "              |  |              ",#(14,16), (14 ,17)
            "                                ",
        ]
        super().__init__(stdscr, input_handler, height=18, width=64, display=house)
        self.x=x
        self.y=y

        self.entity = Entity(self.window, self.y, self.x, "@")
        
    def get_window_data(self):
       pass
    
    def render(self, Box=False, Walls=False):
        

    
        for y in range(self.height-1):
            for x in range(self.width):
                self.window.addstr(y, x, ';')
        
            
        super().render(Box=Box, Walls=Walls)
   

        self.window.refresh()
        self.entity.draw()
        self.window.refresh()

    def animate_scene1st(self):
        self.window.refresh()
        for i in range(5):
            self.entity.move('up', self.walls)
            self.window.refresh()
            time.sleep(0.08)
        
        self.render()


    def should_exit(self):
        # Define exit condition: player should be in a specific position
        if self.entity.position() == (15 + self.entity.begin_y, 32 + self.entity.begin_x) or self.entity.position() == (15 + self.entity.begin_y, 31 + self.entity.begin_x):
            return True





