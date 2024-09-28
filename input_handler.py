import curses

class InputHandler:
    
    def __init__(self, stdscr: curses.window):
        """
        Initialize the InputHandler class.

        :param stdscr: is the main window object from curses.
        """
        self.stdscr = stdscr

    def handle_input(self, window):
        """
        Determine the type of window and handle input accordingly.

        :param window: is the window object for which input is being handled.
        :return: is the result of input handling, which can vary based on window type.
        """
        import windows
        import display_windows

        if isinstance(window, windows.Menu_Window):
            return self.handle_menu_input(window)
        elif isinstance(window, display_windows.NameBox):
            return self.handle_name_box_input(window)
        elif isinstance(window, display_windows.ExitWindow):
            return self.handle_exit_window_input(window)
        elif isinstance(window, display_windows.House_Window):
            return self.handle_house_window_input(window)
        elif isinstance(window, display_windows.Narration_Window):
            return self.handle_narration_window_input(window)
        elif isinstance(window, display_windows.Battle_Window):
            return self.handle_battle_window_input(window)
        else:
            raise ValueError("Unknown window type")

    def handle_menu_input(self, menu_window):
        """
        Handle user input for the menu window.

        :param menu_window: is the menu window object where input is being handled.
        :return: is the selected menu option based on user input.
        """
        key = self.stdscr.getch()

        if key == curses.KEY_UP and menu_window.selected_row_index > 0:
            # Move selection up if possible
            menu_window.selected_row_index -= 1
        elif key == curses.KEY_DOWN and menu_window.selected_row_index < len(menu_window.menu) - 1:
            # Move selection down if possible
            menu_window.selected_row_index += 1
        elif key == ord('\n'):
            # Return the selected menu option when Enter is pressed
            return menu_window.menu[menu_window.selected_row_index]
        return None

    def handle_name_box_input(self, name_box):
        """
        Handle user input for the name box window.

        :param name_box: is the name box window object where input is being handled.
        :return: is the text input by the user, validated and trimmed.
        """
        def validate_key(ch):
            # Convert carriage return to newline if needed
            return 7 if ch == 10 else ch

        name = name_box.text_box.edit(validate_key).strip()
        name_box.clear_and_refresh()
        return name

    def handle_exit_window_input(self, exit_window):
        """
        Handle user input for the exit window.

        :param exit_window: is the exit window object where input is being handled.
        """
        key = exit_window.stdscr.getch()
        if key in (ord('y'), ord('Y')):
            # Exit the program if 'y' or 'Y' is pressed
            raise SystemExit()
        elif key in (ord('n'), ord('N')):
            # Close the exit window if 'n' or 'N' is pressed
            exit_window.clear_and_refresh()

    def handle_house_window_input(self, house_window):
        """
        Handle user input for the house window.

        :param house_window: is the house window object where input is being handled.
        :return: is the result of the input action, if applicable.
        """
        key = house_window.window.getch()

        if key == ord('q'):
            # Return 'q' if 'q' is pressed
            return 'q'
        

        # Move the entity based on arrow key input and refresh the window
        if key == curses.KEY_UP:
            house_window.entity.move('up', house_window.walls)
            house_window.entity.window.refresh()
        elif key == curses.KEY_DOWN:
            house_window.entity.move('down', house_window.walls)
            house_window.entity.window.refresh()
        elif key == curses.KEY_LEFT:
            house_window.entity.move('left', house_window.walls)
            house_window.entity.window.refresh()
        elif key == curses.KEY_RIGHT:
            house_window.entity.move('right', house_window.walls)
            house_window.entity.window.refresh()

    def handle_narration_window_input(self, narration_window):
        """
        Handle user input for the narration window.

        :param narration_window: is the narration window object where input is being handled.
        :return: is 's' if Enter is pressed, otherwise None.
        """
        key = narration_window.window.getch()
        if key == ord('\n'):
            return 's'
        return None

    def handle_battle_window_input(self, battle_window):
        """
        Handle user input for the battle window, including player movement and viewport scrolling.

        :param battle_window: is the battle window object where input is being handled.
        """
        # Draw the entity in the battle window
        battle_window.entity.draw()

        # Capture user input
        key = battle_window.stdscr.getch()

        # Move the player based on arrow key input and refresh the viewport
        if key == curses.KEY_UP and battle_window.entity.y > 0:
            battle_window.entity.move('up', battle_window.walls)
            battle_window.window.refresh(battle_window.view_y, battle_window.view_x, battle_window.viewport_start_y, battle_window.viewport_start_x, battle_window.view_height - 1, battle_window.view_width - 1)
        elif key == curses.KEY_DOWN and battle_window.entity.y < len(battle_window.maze) - 1:
            battle_window.entity.move('down', battle_window.walls)
            battle_window.window.refresh(battle_window.view_y, battle_window.view_x, battle_window.viewport_start_y, battle_window.viewport_start_x, battle_window.view_height - 1, battle_window.view_width - 1)
        elif key == curses.KEY_LEFT and battle_window.entity.x > 0:
            battle_window.entity.move('left', battle_window.walls)
            battle_window.window.refresh(battle_window.view_y, battle_window.view_x, battle_window.viewport_start_y, battle_window.viewport_start_x, battle_window.view_height - 1, battle_window.view_width - 1)
        elif key == curses.KEY_RIGHT and battle_window.entity.x  < len(battle_window.maze[0]) - 1:
            battle_window.entity.move('right', battle_window.walls)
            battle_window.window.refresh(battle_window.view_y, battle_window.view_x, battle_window.viewport_start_y, battle_window.viewport_start_x, battle_window.view_height - 1, battle_window.view_width - 1)
        elif key == ord('q'):
            return 'q'
        

        # Scroll the viewport when the player reaches the edges
        if battle_window.entity.y - battle_window.view_y < 5 and battle_window.view_y > 0:
            battle_window.view_y -= 1
        elif battle_window.entity.y + battle_window.viewport_start_y - battle_window.view_y > battle_window.view_height - 5 and battle_window.view_y < len(battle_window.maze)*2 - battle_window.view_height:
            battle_window.view_y += 1
        if battle_window.entity.x - battle_window.view_x < 25 and battle_window.view_x > 0:
            battle_window.view_x -= 1
        elif battle_window.entity.x + battle_window.viewport_start_x - battle_window.view_x > battle_window.view_width - 25 and battle_window.view_x < len(battle_window.maze[0])*2 - battle_window.view_width:
            battle_window.view_x += 1

        # Redraw the entity and refresh the viewport
        battle_window.entity.draw()
        battle_window.window.refresh(battle_window.view_y, battle_window.view_x, battle_window.viewport_start_y, battle_window.viewport_start_x, battle_window.view_height - 1, battle_window.view_width - 1)
