import pickle

class GameState:
    def __init__(self, player_position, scene, window_data=None, inventory=None):
        self._player_position = player_position
        self._scene = scene
        self._window_data = window_data if window_data is not None else {}
        self.inventory = inventory if inventory is not None else {}

    def get_current_scene(self):
        return self._scene

    def set_current_scene(self, new_scene):
        self._scene = new_scene

    def get_player_position(self):
        return self._player_position

    def set_player_position(self, new_player_position):
        self._player_position = new_player_position

    def get_window_data(self):
        return self._window_data

    def set_window_data(self, window_data):
        self._window_data = window_data

    def save(self, filename="savefile.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename="savefile.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None
