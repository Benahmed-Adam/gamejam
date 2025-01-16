from utils.settings import *
from utils.utils import Utils
from game.gamestate import GameState
from game.particles import Particules
from game.menu import Menu
from game.game import Chepa

class Main:
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"
        pg.init()
        self.screen = pg.display.set_mode((0,0),pg.FULLSCREEN)
        self.utils = Utils(self)
        self.settings = Settings(self)
        self.settings.update_settings()
        self.particules = Particules(self)
        self.menu = Menu(self)
        self.game = Chepa(self)
        self.state = GameState(self, {
            "main_menu": [self.menu.main_menu, self.utils.menu_sound],
            "parametre_menu": [self.menu.settings, self.utils.menu_sound],
            "audio_menu": [self.menu.audio, self.utils.menu_sound],
            "resolution_menu" : [self.menu.resolution, self.utils.menu_sound],
            "howtoplay" : [self.menu.howtoplay, self.utils.menu_sound],
            "game": [self.game.play, self.utils.game_sound],
            "win" : [self.game.win, self.utils.win_sound],
            "loose_chevalier" : [self.game.loose_message, self.utils.loose_chevalier_sound],
            "loose_pirate" : [self.game.loose_message, self.utils.loose_pirate_sound],
        })
        self.state.modify_state("main_menu")
        pg.mouse.set_visible(False)
        self.clock = pg.time.Clock()
        self.FPS = 60
        pg.display.set_caption("jeu de qualité")

    def run(self):
        while True:
            self.state.run_current_function()

if __name__ == "__main__":
    game = Main()
    game.run()