# Labyrinths



#### Description:
Labyrinths is a terminal-based rogue-like game built using Python and the `curses` module. The player embarks on a mysterious journey through multiple labyrinths, where each maze becomes increasingly complex. The game is navigated using the **arrow keys**, and the **Enter key** is used for interactions. The objective is to find your way out of the maze while experiencing an eerie, time-warping storyline.

#### Project Structure:
1. **`game.py`**
   - This is the core file of the game, containing the **main game loop**. It initializes all scenes, such as the labyrinths, house scenes, and battle scenes.
   - Includes an **unfinished save/load feature**, which will allow players to save their progress and resume later.
   - The game transitions between different scenes, manages player input, and controls the flow of the story.

2. **`input_handler.py`**
   - Manages player input, specifically listening for the **arrow keys** to move the character and the **Enter key** for interactions.
   - Each scene in the game responds to player input via this handler, whether navigating through the maze or interacting with objects.

3. **`entity.py`**
   - Defines the **player character** and how they interact with the environment.
   - Prevents the player from passing through walls and lays the foundation for future additions of NPCs or enemies.

4. **`utils.py`**
   - Contains **utility arrays** used for the labyrinth layouts. These arrays are essentially the blueprints for the mazes that the player navigates.
   - The arrays are referenced in the game loop to update the screen with the current state of the labyrinth.

5. **`game_state.py`**
   - Created for the planned **save/load feature**. It uses the **`pickle` module** to serialize and deserialize game objects, allowing the player to save their current progress and resume from the same point.
   - **Pickle**: A Python library for converting Python objects into a binary format and storing them in files, which can be reloaded later.

6. **`windows.py`**
   - Defines the basic **Window class**, used for managing different windows in the game. This includes windows for the **menu**, **narration**, and **battle scenes**.
   - Each window allows for easy manipulation of terminal output, making it simple to manage different parts of the screen.

7. **`display_windows.py`**
   - Extends the `Window` class to handle more complex displays like the **exit window**, **narration box window**, and **house window**.
   - These windows require more advanced functionality than the basic `Window` class, hence the need for this separate class hierarchy.

8. **`test_project.py`**
   - Basic test cases were created to satisfy the project requirements but are not fully developed.
   - The testing framework sets the groundwork for future test expansion, focusing on ensuring that game functionality operates as expected.

#### Mechanics and Design:
- **Game Engine**: The game is built using Python’s `curses` module, allowing for low-level control of terminal input and output. This provides a simple but effective environment for a text-based game.
- **Window Management**: The game uses two primary window classes (`Window` and `DisplayWindow`) to manage the different terminal scenes. These windows control everything from the menu to labyrinth exploration.
- **Terminal Sizing**: The game includes basic functionality to detect and handle changes in terminal size. However, significant resizing of the terminal could still disrupt the display.

#### How to Play:
- Use the **arrow keys** to navigate through the labyrinth.
- Press **Enter** to interact with objects and progress through the game’s story.
- Explore multiple labyrinths, avoid dead ends, and try to find your way out.

#### Soundtrack:
- The game includes **3 custom soundtracks** and **1 sound effect**, composed using [Beepbox.com](https://beepbox.co/). The sound helps enhance the otherwise minimalistic visual experience by adding atmosphere and emotion to the game.

#### Future Improvements:
- **Save/Load Feature**: This will allow players to save their progress and resume from the same point.
- **Enhanced Testing**: More comprehensive unit testing will be added to ensure the stability of the game’s mechanics.

#### Backstory:
The protagonist, lost in thought after receiving a letter, accidentally stumbles into a labyrinth while out for a walk in the forest. As the door behind him slams shut, the player has no choice but to venture deeper into the maze, hoping to find another exit. But each labyrinth becomes more twisted, and upon finally finding an exit, the player realizes something strange — it’s as if time hasn’t passed at all.
