import curses
import threading
import time
import sys
from game import Game

MIN_HEIGHT, MIN_WIDTH = 24, 80  # Minimum terminal size

def check_terminal_size(stdscr, exit_event):
    """Continuously monitors the terminal size for resizing."""
    previous_size = stdscr.getmaxyx()  # Get the initial terminal size

    while not exit_event.is_set():  # Continue looping until exit_event is set
        current_size = stdscr.getmaxyx()  # Check the current terminal size
        if current_size != previous_size:  # If the size has changed
            previous_size = current_size  # Update the previous size
            # Check if the current size is below minimum dimensions
            if current_size[0] < MIN_HEIGHT or current_size[1] < MIN_WIDTH:
                
                display_resize_warning(stdscr) 
                exit_event.set()
                sys.exit()
                  # Signal to exit the main thread

        time.sleep(2)  # Sleep for a second to avoid busy waiting

def display_resize_warning(stdscr):
    """Displays a warning if the terminal size is too small."""
    stdscr.clear()  # Clear the screen for the warning message
    stdscr.addstr(0, 0, "Terminal size is too small. Kindly press a key.", curses.A_BOLD)  # Display the warning
    stdscr.refresh()
    
     # Refresh the screen to show the message
      # Wait for a few seconds before returning

def main(stdscr):
    """Entry point to run the curses-based game."""
    curses.curs_set(0)  # Hide the cursor for a cleaner interface
    exit_event = threading.Event()  # Initialize the exit event to control thread termination
    # Start the thread that monitors the terminal size
    resize_thread = threading.Thread(target=check_terminal_size, args=(stdscr, exit_event))
    resize_thread.daemon = True  # Set the thread as a daemon to allow program exit
    resize_thread.start()  # Start the monitoring thread

    try:
        game = Game(stdscr)  # Initialize the game
        game.run()  # Run the game's main loop
    except curses.error as e:
        handle_initialization_error(stdscr, e)  # Handle any curses-related errors

     # Exit the program cleanly

def handle_initialization_error(stdscr, error):
    """Handles initialization errors by displaying a warning message."""
    stdscr.clear()  # Clear the screen for the error message
    stdscr.addstr(0, 0, f"Initialization error: {error}. Kindly resize the terminal and rerun.", curses.A_BOLD)  # Display the error
    stdscr.refresh()  # Refresh the screen to show the message
    time.sleep(2)  # Wait for a moment before exiting
    sys.exit()  # Exit the program

if __name__ == "__main__":
    curses.wrapper(main)  # Start the curses application
