Labyrinths
Labyrinths is a terminal-based rogue-like game built using Python and the curses module. It takes the player on a mysterious journey through a series of labyrinths, each one more complex than the last. Along the way, the character uncovers the eerie nature of the maze and realizes that nothing is as it seems.

Table of Contents
Gameplay
Project Structure
Mechanics and Design
Installation and Requirements
How to Play
Soundtrack
Future Improvements
Backstory
Video Demo
Gameplay
Navigate the labyrinths using only the arrow keys and interact with the game using the Enter key. The game is all about careful exploration, and your main challenge will be figuring out how to escape the twisting paths of the maze while avoiding dead ends.

Project Structure
Files:
game.py

This is the main file of the game, where all the action happens. It contains the main game loop and is responsible for initializing and managing the different scenes such as labyrinths, the player's home, and battle scenes. The save/load feature is partially implemented in this file but remains unfinished.
The game initializes by setting up all the window scenes and the initial labyrinth. This file contains key logic for transitioning between scenes, such as entering or exiting a labyrinth or battling within the maze.
The game loop handles player movement, interaction with the environment, and how the scenes change based on player decisions.
input_handler.py

This file handles the input mechanism for the game. It listens for keyboard inputs from the player, specifically arrow keys for movement and the Enter key for interactions.
It allows different windows and game scenes to respond to specific key presses. For example, the arrow keys navigate through the labyrinth, while the Enter key interacts with doors or starts dialogue sequences.
entity.py

This file defines the player object and handles interactions with the environment. It ensures that the player character does not pass through walls and can navigate the maze properly.
In this version of the game, only the player object is implemented, but the structure is designed to support additional entities, such as enemies or NPCs, in the future. These could be easily integrated using the same class architecture.
utils.py

Contains utility arrays, most notably the layouts of the labyrinths used in the game. These labyrinths are pre-determined and displayed as a grid of characters, with walls and paths created using keyboard symbols.
The utility arrays are referenced in the game loop to update and render the current state of the maze on the screen, giving the player a visual representation of their progress through the labyrinth.
game_state.py

Currently unused, but this file was created for the save/load feature. It utilizes the pickle module to serialize and deserialize game state data.
The pickle module is a Python library that allows saving objects (such as the game state, player position, and labyrinth progress) in a binary format. Later, these objects can be reloaded from disk, allowing the player to resume from where they left off.
Though this feature is unfinished, the groundwork for saving player progress is laid out here.
windows.py

Defines the Window class and its child windows like the menu window, narration window, and battle window. This class allows for easy manipulation of different parts of the terminal screen, depending on the scene.
The Window class abstracts much of the complexity involved in managing the terminal display. It allows for quick rendering, clearing, and updating of different windows that represent in-game elements such as text narration or battles.
display_windows.py

Extends the Window class to create additional windows that handle more complex scenes such as the exit window, anem box window, and house window.
The DisplayWindow class is more specialized and contains additional logic needed for certain scenes, particularly those with more intricate interactions or animations. This structure allows the DisplayWindow class to inherit base functionality from Window, while adding unique features where necessary.
test_project.py

This file was created to satisfy the project requirements but is not extensively utilized. It contains some basic tests for checking functionality, but future iterations of the project will require more robust testing practices.
Although minimal, this file sets up the framework for future unit testing to ensure that all game components are functioning as expected.
Sound:
The project includes 3 soundtracks and 1 sound effect. These were composed using Beepbox.com, adding a unique auditory experience to the otherwise text-based gameplay.
The soundtracks add atmosphere, helping to offset the minimalistic visual style that relies on simple keyboard characters to represent the game's environment.
Mechanics and Design
Game Engine
The game was built using the Python curses module, which allows interaction with the terminal screen. This choice of engine keeps the design low-level, allowing for direct control over the display and keyboard input.

Window Management
Two classes were built to handle the different types of windows:

The Window class manages basic windows, including the menu, narration, and battle windows. These windows provide text-based interaction and feedback to the player.
The DisplayWindow class extends Window to include more specific windows, such as the exit window or house window, which have additional functionality required for scene transitions.
Terminal Sizing Control
To maintain the integrity of the game's visuals, resizing the terminal is discouraged. The game includes functions that detect terminal size changes and handle them gracefully, though if the terminal is significantly resized, it can still disrupt the game’s display.

Installation and Requirements
To run the game, make sure you have Python and the curses module installed.

Clone this repository.
Run the game with:
bash
Copy code
python game.py
How to Play
Use the arrow keys to move the character through the labyrinths.
Press Enter to interact with objects and progress through the story.
Navigate through multiple labyrinths, each more challenging than the last, to find your way out.
Soundtrack
The music was composed by ear using Beepbox.com. The inclusion of sound significantly enhances the mood and atmosphere of the game, providing auditory cues to match the mysterious labyrinth environment.

Future Improvements
Save/Load Feature: As mentioned, the save/load functionality is still under development and will use the pickle module for serialization.
Enhanced Testing: More thorough testing is planned for future updates, as the current test_project.py file contains only basic test cases.
Backstory
The protagonist embarks on a walk through the forest to clear his mind after receiving a troubling letter. Lost in thought, he accidentally enters a labyrinth. The door slams shut behind him, locking him inside. The only way forward is through the twisting, convoluted paths of the labyrinths. Each labyrinth becomes more challenging, but there is hope for an exit. However, upon reaching what seems to be freedom, the character realizes that he has returned home — but something is off. (Hint: time-warping is involved.)

Video Demo
Watch the game demo here: Video Link

