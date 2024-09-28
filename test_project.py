import pytest # type: ignore
import curses
import threading
from unittest.mock import MagicMock
from project import check_terminal_size, display_resize_warning, handle_initialization_error  # Adjust the import as needed

def test_check_terminal_size(mocker):
    """Test check_terminal_size for terminal resizing."""
    stdscr = mocker.MagicMock()
    mocker.patch('time.sleep', return_value=None)
    exit_event = threading.Event()  # Use a real threading event

    # Simulate initial terminal size
    stdscr.getmaxyx.side_effect = [(24, 80), (13, 50)]  # Initial size and resized below minimum

    # Start the terminal size check in a thread
    check_thread = threading.Thread(target=check_terminal_size, args=(stdscr, exit_event))
    check_thread.start()

    # Wait for the exit_event to be set (indicating the warning was shown)
    exit_event.wait(timeout=2)  # Wait up to 2 seconds

      # Ensure exit_event is set due to small size
    stdscr.addstr.assert_called_once_with(
        0, 0, "Terminal size is too small. Kindly press a key.", curses.A_BOLD
    )
    assert exit_event.is_set()


def test_display_resize_warning():
    """Test display_resize_warning displays the warning message."""
    stdscr = MagicMock()
    display_resize_warning(stdscr)

    stdscr.clear.assert_called_once()
    stdscr.addstr.assert_called_once_with(
        0,
        0,
        "Terminal size is too small. Kindly press a key.",
        curses.A_BOLD  # Use this directly as a constant
    )
    stdscr.refresh.assert_called_once()

def test_handle_initialization_error():
    """Test handle_initialization_error displays an error message."""
    stdscr = MagicMock()
    error_message = "Some error occurred."

    with pytest.raises(SystemExit):  # Catch the SystemExit exception
        handle_initialization_error(stdscr, error_message)

    stdscr.clear.assert_called_once()
    stdscr.addstr.assert_called_once_with(
        0,
        0,
        f"Initialization error: {error_message}. Kindly resize the terminal and rerun.",
        curses.A_BOLD  # Use this directly as a constant
    )
    stdscr.refresh.assert_called_once()