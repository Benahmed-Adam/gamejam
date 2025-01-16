from utils.settings import *

class GameState:

    def __init__(self, game, states: dict) -> None:
        self.game = game
        self.states = states
        self.current_state = []
        self.current_song = None
    
    def modify_state(self, key : str):
        self.current_state.append(key)

    def lower_state(self):
        self.current_state.pop()

    def update_song(self):
        new_song = self.states[self.current_state[-1]][1]
        if new_song != self.current_song and new_song is not None:
            if self.current_song is not None:
                self.current_song.stop()
            new_song.play(-1)
            self.current_song = new_song

    def run_current_function(self):
        self.update_song()
        self.states[self.current_state[-1]][0]()