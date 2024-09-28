import curses

class Entity:
    def __init__(self, window: curses.window, y: int, x: int, char: str = "@"):
        self.window = window
        self.y = y
        self.x = x
        self.char = char
        self.begin_y, self.begin_x = self.window.getbegyx()

    def draw(self):
        self.window.addch(self.y, self.x, self.char)

    def move(self, direction, walls):
        max_y, max_x = self.window.getmaxyx()
        new_y, new_x = self.y, self.x

        if direction == 'up':
            new_y -= 1
        elif direction == 'down':
            new_y += 1
        elif direction == 'left':
            new_x -= 1
        elif direction == 'right':
            new_x += 1

        # Check wether the new position is within the wall boundaries and within the screen
        if (new_y, new_x) not in walls and 0 < new_y < max_y - 1 and 0 < new_x < max_x - 1:
            # Erase the character from the old position
            self.window.addch(self.y, self.x, " ")
            self.y, self.x = new_y, new_x
            self.draw()

    def position(self):
        return (self.y + self.begin_y, self.x + self.begin_x)
