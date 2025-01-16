from utils.settings import *

class Utils:
    def __init__(self, game) -> None:
        self.game = game
        self.font = pg.font.Font(None, 40)
        self.mouse_texture = pg.image.load("ressources/mouse.png").convert_alpha()
        self.mouse_texture.set_colorkey((0, 0, 0, 0))      
        self.effect_button_sound = pg.mixer.Sound("ressources/button_effect.mp3")
        self.menu_sound = pg.mixer.Sound("ressources/menu_theme.mp3")
        self.error_sound = pg.mixer.Sound("ressources/error.mp3")
        self.game_sound = pg.mixer.Sound("ressources/cirque.mp3")
        self.win_sound = pg.mixer.Sound("ressources/win.mp3")
        self.loose_chevalier_sound = pg.mixer.Sound("ressources/loose_chevalier.mp3")
        self.loose_pirate_sound = pg.mixer.Sound("ressources/loose_pirate.mp3")

        with open("data/settings.json", "r") as data:
            self.settings_data = json.load(data)
    
    def update_mouse(self):
        self.game.screen.blit(self.mouse_texture, pg.mouse.get_pos())
    
    def get_fps(self):
        self.font = pg.font.Font(None, int(40 * self.game.settings.SCALE_FACTOR_WIDTH))
        text1 = self.font.render(f"FPS : {int(self.game.clock.get_fps())}", True, (255, 255, 255))
        rect1 = text1.get_rect(center=(1860 * self.game.settings.SCALE_FACTOR_WIDTH, 20 * self.game.settings.SCALE_FACTOR_HEIGHT))
        self.game.screen.blit(text1, rect1)
    
    def save_settings(self):
        with open("data/settings.json","w") as data:
            json.dump(self.settings_data,data,indent=2)