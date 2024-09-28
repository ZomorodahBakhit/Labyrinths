import curses
import time
from pygame import mixer


from windows import Menu_Window
from display_windows import ExitWindow, NameBox, House_Window, Narration_Window, Battle_Window
from input_handler import InputHandler
from game_state import GameState
import utils



# (Global) flag for pause
GAME_PAUSED = False





def setup_game():
    """
    Initializes a new game and returns a message indicating completion.
    """
    # This could be expanded to include actual setup logic
    return "Game setup complete"

def save_game_state(game):
    """
    Saves the current game state to a file.
    """
    try:
        with open('game_save.txt', 'w') as file:
            file.write(f"scene:{game.get_current_scene()}\n")
            file.write(f"position:{game.get_player_position()}\n")
            # Write any other relevant game state information here
        return "Game state saved"
    except Exception as e:
        return f"Failed to save game state: {e}"

def load_game_state():
    """
    Loads the game state from a file and returns a message indicating the result.
    """
    try:
        with open('game_save.txt', 'r') as file:
            lines = file.readlines()
            scene = lines[0].strip().split(':')[1]
            position = tuple(map(int, lines[1].strip().split(':')[1].strip().split(',')))
            # Parse any other relevant game state information here

        # For simplicity, we'll just return the loaded data
        return f"Game state loaded: scene={scene}, position={position}"
    except Exception as e:
        return f"Failed to load game state: {e}"
    



class Game:
    def __init__(self, stdscr):
        """
        Initialize the game with windows, an input handler, and a game state.
        """
        self.stdscr = stdscr
        self.input_handler = InputHandler(stdscr)
        self.menu_window = Menu_Window(stdscr, self.input_handler)
        self.exit_window = ExitWindow(stdscr, self.input_handler)
        
        # Initialize house and battle scenes
        self.house_window_1 = House_Window(stdscr, self.input_handler)
        self.house_window_2 = House_Window(stdscr, self.input_handler, x=32, y=16)  

        # Initialize battle scenes
        self.battle_window_1 = Battle_Window(stdscr, self.input_handler, utils.maze1, 0, 30, 6, 59)
        self.battle_window_10 = Battle_Window(stdscr, self.input_handler, utils.maze10, 0, 30, 6, 63)
        self.battle_window_2 = Battle_Window(stdscr, self.input_handler, utils.maze2, 10, 90, 15, 150)
        self.battle_window_3 = Battle_Window(stdscr, self.input_handler, utils.maze3, 0, 85, 4, 125)
        
        self.skull_narration_count = False
        
        # Initial game state
        self.state = GameState(player_position=None, scene="house_scene_1")  # Start in the first house scene

    # State functions
    def get_current_scene(self):
        return self.state.get_current_scene()

    def set_current_scene(self, new_scene):
        self.state.set_current_scene(new_scene)

    def set_player_position(self, new_player_position):
        self.state.set_player_position(new_player_position)

    def get_player_position(self):
        return self.state.get_player_position()

    # Save and load game functions
    def save_game(self):
        """
        This saves the current state of the game.
        """
        save_message = save_game_state(self)
        print(save_message)  # Replace with appropriate logging or messaging

    def load_game(self):
        """
        This loads the saved game state and restores the game based on the saved scene and data.
        """
        load_message = load_game_state()
        print(load_message)  # Replace with appropriate logging or messaging
        if load_message.startswith("Game state loaded"):
            scene, position = load_message.split(': ')[1].split(', ')
            self.set_current_scene(scene)
            self.set_player_position(tuple(map(int, position.strip()[1:-1].split(','))))
            self.restore_game_state()

    def restore_game_state(self):
        """
        This restores the game based on the current scene stored in the game state.
        """
        current_scene = self.get_current_scene()
        if current_scene == "house_scene_1":
            self.house_window_1.get_window_data()
            self.house_window_1.render()
        elif current_scene == "house_scene_2":
            self.house_window_2.get_window_data()
            self.house_window_2.render()
        elif current_scene == "battle_scene_1":
            self.battle_window_1.get_window_data()
            self.battle_window_1.render()
        elif current_scene == "battle_scene_2":
            self.battle_window_2.set_window_data(self.state.get_window_data())
            self.battle_window_2.render()
        elif current_scene == "battle_scene_3":
            self.battle_window_3.set_window_data(self.state.get_window_data())
            self.battle_window_3.render()

    # Pause and menu handling
    def handle_loop_and_exit_menu(self, window_playing):
        """
        This handles the game loop and displays the exit menu when the game is paused.
        """
        window_playing.window.keypad(True)
        global GAME_PAUSED

        if GAME_PAUSED:
            self.exit_window.render()
            self.exit_window.handle_input()
            self.exit_window.clear_and_refresh
            window_playing.render()
            GAME_PAUSED = False
        else:
            key = window_playing.handle_input()
            if key == 'q':
                GAME_PAUSED = True
            else:
                window_playing.handle_input()

    def run(self):
        """
        This starts the game, initializes the mixer for background music, and handles the menu system.
        """
        mixer.init()
        mixer.music.load("Morning.mp3")
        mixer.music.play(-1)

        self.menu_window.render()

        while True:
            option = self.menu_window.handle_input()

            if option == "Quit":
                self.exit_window.render()
                self.exit_window.handle_input()
                self.menu_window.clear_and_refresh()
                self.menu_window.render_open_scroll()
                self.menu_window.render_menu()
                self.stdscr.refresh()

            elif option == "Continue":
                pass  # Continue from saved game

            elif option == "New Game":
                self.start_new_game()
                self.skull_narration_count = False
                self.run()

            elif option == "Settings":
                pass  # Handle settings

            else:
                self.menu_window.render()

    # The new game start and the main game loop
    def start_new_game(self):
        """
        Start a new game from the beginning.
        """
        self.menu_window.clear_and_refresh()

        # This is character creation and initial setup
        curses.curs_set(1)
        name_box = NameBox(self.stdscr, self.input_handler)
        name_box.render()
        name = name_box.handle_input()
        curses.curs_set(0)
        name_box.clear_and_refresh()

        # Initialize the first scene of the new game
        self.set_current_scene("house_scene_1")
        self.house_window_1.stdscr.refresh()
        self.house_window_1.render(Box=True, Walls=True)

        # Display initial narrative
        narration_box = Narration_Window(self.stdscr, self.input_handler, name)
        narration_box.render_narration("“Time is a fickle thing.”\n\n                                Press 'Enter'")
        time.sleep(0.5)
        narration_box.render_narration("What could she have meant by that?")
        time.sleep(0.5)
        narration_box.render_narration("It is already 5:00.\n")
        narration_box.render_narration("(sighs) I am getting way too in my head.\n")
        narration_box.render_narration("I'll probably take a walk in the forest.\nIt'll help get my mind off things a little.")

        # This is the main game loop for first scene
        self.main_game_loop(self.house_window_1)
        self.house_window_1.entity.y = self.house_window_1.y
        self.house_window_1.entity.x = self.house_window_1.x
        self.house_window_1.clear_and_refresh()

        time.sleep(2)

        # Transition to the first battle scene
        self.set_current_scene("battle_scene_1")
        self.battle_window_10.render()

        narration_box2 = Narration_Window(self.stdscr, self.input_handler, name, 5, 70, True)
        narration_box2.render_narration("Huh? What is this place?")
        time.sleep(0.5)
        narration_box2.render_narration("I must have taken a wrong turn.")
        mixer.music.stop()
        time.sleep(0.5)
        mixer.music.load("Dark.mp3")
        mixer.music.play(-1)

        narration_box2.render_narration("It is pretty dark and creepy.")
        narration_box2.render_narration("I should probably head back.")

        # Play through battle_scene_1
        self.battle_window_1.render()
        
        mixer.music.load("Door_Slam.mp3")
        mixer.music.play()

        narration_box2.render_narration("AHHH!?")

        self.battle_window_1.entity.move("right", self.battle_window_1.walls)
        self.battle_window_1.window.refresh(self.battle_window_1.view_y, self.battle_window_1.view_x, self.battle_window_1.viewport_start_y, self.battle_window_1.viewport_start_x, self.battle_window_1.view_height - 1, self.battle_window_1.view_width - 1)

        narration_box2.render_narration("HEYYY!!\nOPEN THE DOOR!!!")

        self.battle_window_1.entity.move("right", self.battle_window_1.walls)
        self.battle_window_1.window.refresh(self.battle_window_1.view_y, self.battle_window_1.view_x, self.battle_window_1.viewport_start_y, self.battle_window_1.viewport_start_x, self.battle_window_1.view_height - 1, self.battle_window_1.view_width - 1)

        narration_box2.render_narration("Is someone playing a joke on me?")
        narration_box2.render_narration("I do not have time for this.\nThis is'nt funny.")

        mixer.music.load("Dark.mp3")
        mixer.music.play(-1)

        self.battle_window_1.entity.move("left", self.battle_window_1.walls)
        self.battle_window_1.window.refresh(self.battle_window_1.view_y, self.battle_window_1.view_x, self.battle_window_1.viewport_start_y, self.battle_window_1.viewport_start_x, self.battle_window_1.view_height - 1, self.battle_window_1.view_width - 1)

        self.battle_window_1.entity.move("left", self.battle_window_1.walls)
        self.battle_window_1.window.refresh(self.battle_window_1.view_y, self.battle_window_1.view_x, self.battle_window_1.viewport_start_y, self.battle_window_1.viewport_start_x, self.battle_window_1.view_height - 1, self.battle_window_1.view_width - 1)

        time.sleep(.9)

        narration_box2.render_narration("(sighs) It is alright. There must be another exit.")
        narration_box2.render_narration("I should just keep calm.")

        
        

    
        self.main_game_loop(self.battle_window_1)
        mixer.music.stop()
        self.battle_window_1.entity.y=self.battle_window_1.player_y
        self.battle_window_1.entity.x=self.battle_window_1.player_x


        # Play through battle_scene_2

        self.set_current_scene("battle_scene_2")
        self.battle_window_2.render()
        time.sleep(1)
        mixer.music.load("Jazz.mp3")
        mixer.music.play(-1)

        
        narration_box2.render_narration("This place just keeps getting weirder.")
        time.sleep(0.5)
        narration_box2.render_narration("How do I even get out of here?")
        time.sleep(0.5)
        narration_box2.render_narration("There has to be a way out.")
        time.sleep(0.5)

        
        self.main_game_loop(self.battle_window_2)
        mixer.music.stop()
        self.battle_window_2.entity.y=self.battle_window_2.player_y
        self.battle_window_2.entity.x=self.battle_window_2.player_x

    

        # Transition to the third battle scene

        self.set_current_scene("battle_scene_3")
        self.battle_window_3.render()
        time.sleep(1)
        mixer.music.load("Knock.mp3")
        mixer.music.play(-1)

        # Play through battle_scene_3

        
        narration_box2.render_narration("I must be close to the end now.")
        time.sleep(0.5)
        narration_box2.render_narration("This place feels different. Is it... colder?")
        time.sleep(0.5)
        narration_box2.render_narration("I am not sure how much longer I can go.")
        time.sleep(0.5)

        
        while True:
            self.handle_loop_and_exit_menu(self.battle_window_3)
            if self.battle_window_3.should_exit():
                break
            elif self.battle_window_3 == self.battle_window_3 and not self.skull_narration_count:
                if self.battle_window_3.entity.position() == (32, 75):
                    self.skull_narration_count = True
                    narration_box2.render_narration("???")
                    time.sleep(.5)
                    narration_box2.render_narration("Why is there a skull engraved on the floor?")
                    time.sleep(.9)
                    narration_box2.render_narration("I am really hoping this was simply a design choice.")
                    break
        self.main_game_loop(self.battle_window_3)
        # Transition to final house scene and loop back

        self.set_current_scene("house_scene_2")
        self.house_window_2.render()
        self.house_window_2.animate_scene1st()

        
        narration_box2.render_narration("How am I back here?")
        time.sleep(0.5)
        
    
        narration_box2.render_narration("What happened?")
        
        mixer.music.stop()
        narration_box2.render_narration("What is the time?")
        time.sleep(0.5)



    def main_game_loop(self, window_playing):
        """
        The core game loop for each scene.
        """
        while True:
            self.handle_loop_and_exit_menu(window_playing)
            if window_playing.should_exit():
                break
            elif window_playing == self.battle_window_3 and not self.skull_narration_count:
                if self.battle_window_3.entity.position() == (32, 75):
                    self.skull_narration_count = True
                    break

    # This is scene-specific resume functions
    def resume_game(self):
        """
        Resume the game from the saved scene.
        """
        current_scene = self.get_current_scene()
        if current_scene == "house_scene_1":
            self.resume_house_scene_1()
        elif current_scene == "house_scene_2":
            self.resume_house_scene_2()
        elif current_scene == "battle_scene_1":
            self.resume_battle_scene_1()
        elif current_scene == "battle_scene_2":
            self.resume_battle_scene_2()
        elif current_scene == "battle_scene_3":
            self.resume_battle_scene_3()

    def resume_house_scene_1(self):
        """
        Resume the first house scene.
        """
        self.house_window_1.render()
        self.main_game_loop(self.house_window_1)

    def resume_battle_scene_1(self):
        """
        Resume the first battle scene.
        """
        self.battle_window_1.render()
        self.main_game_loop(self.battle_window_1)

# This initialize curses and runs the game
if __name__ == "__main__":
    curses.wrapper(Game)
