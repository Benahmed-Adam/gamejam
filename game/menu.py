from utils.settings import *
from game.ui import Slider, Button, Bandeau, TextZone

class Menu:
    def __init__(self, game) -> None:
        self.game = game
        sr = pg.display.get_surface().get_rect()
        self.veil = pg.Surface(sr.size)
        self.veil.fill((0, 0, 0))
        self._background = pg.image.load("ressources/chevpoulepir.png")
        self.background = pg.transform.scale(self._background, sr.size)
    
    def fadein(self):
        clock = pg.time.Clock()

        for alpha in range(0, 90):
            clock.tick(120)
            self.veil.set_alpha(alpha)
            self.game.screen.blit(self.veil, (0, 0))
            pg.display.flip()
 
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.game.utils.get_fps()
    
    def main_menu(self):
        screen_height = self.game.settings.HEIGHT
        screen_width = self.game.settings.WIDTH
        sfw = self.game.settings.SCALE_FACTOR_WIDTH
        sfh = self.game.settings.SCALE_FACTOR_HEIGHT
        
        self.background = pg.transform.scale(self._background, (1920*sfw, 1080*sfh))

        menu_font_size = int(100 * sfw)
        menu_font = pg.font.Font(None, menu_font_size)
        menu_text = menu_font.render("Jeu de qualité", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(screen_width // 2, screen_height // 10))

        button_height = int(100 * sfw)

        bouton_jouer = Button(self.game, "Jouer", (500 * sfw, button_height), 
                  int(100 * sfw), (screen_width // 2, screen_height // 2 - button_height + 50))
        
        bouton_parametre = Button(self.game, "Paramètres", (500 * sfw, button_height), 
                  int(100 * sfw), (screen_width // 2, screen_height // 2 + 100))
        
        bouton_quitter = Button(self.game, "Quitter", (500 * sfw, button_height), 
                int(100 * sfw), (screen_width // 2, screen_height // 2 + button_height + 150))
        
        bouton_howtoplay = Button(self.game, "Comment jouer", (350 * sfw, button_height), 
                int(50 * sfw), (screen_width - 200 * sfw, 100 * sfh))

        while True:
            self.game.clock.tick(self.game.FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                bouton_quitter.event(event)
                bouton_parametre.event(event)
                bouton_howtoplay.event(event)
                bouton_jouer.event(event)

            self.game.screen.blit(self.background, (0, 0))
            self.game.particules.update_particles()
            self.game.screen.blit(menu_text, menu_rect)
            bouton_quitter.draw()
            bouton_parametre.draw()
            bouton_howtoplay.draw()
            bouton_jouer.draw()
            if bouton_quitter.is_clicked:
                pg.quit()
                sys.exit()
            if bouton_parametre.is_clicked:
                self.game.state.modify_state("parametre_menu")
                return
            if bouton_jouer.is_clicked:
                self.game.state.modify_state("game")
                return
            if bouton_howtoplay.is_clicked:
                self.game.state.modify_state("howtoplay")
                return
            self.game.utils.update_mouse()
            self.game.utils.get_fps()
            pg.display.flip()
    
    def howtoplay(self):
        self.fadein()

        screen_height = self.game.settings.HEIGHT
        screen_width = self.game.settings.WIDTH
        sfw = self.game.settings.SCALE_FACTOR_WIDTH
        sfh = self.game.settings.SCALE_FACTOR_HEIGHT
        
        self.background = pg.transform.scale(self._background, (1920*sfw, 1080*sfh))

        title_font_size = int(60 * sfw)
        title_font = pg.font.Font(None, title_font_size)
        title_text = title_font.render("Comment jouer ?", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 10))

        story_font_size = int(40 * sfw)
        story_font = pg.font.Font(None, story_font_size)
        story_text = [
            "Vous incarnez une poule qui a été capturée par des pirates pour être mangée.",
            "Ils vous ont décapité, mais leur incompétence vous a permis de rester en vie !",
            "Vous avez réussi à vous enfuir, mais maintenant les pirates vous poursuivent.",
            "En chemin, des chevaliers vous ont vu courir sans tête et veulent vous vénérer.",
            "Devenez plus fort en volant l'équipement des chevaliers mort !",
            "Vengez vous et tuez les tous",
            "PS : si un chevalier te touche c game over il te kidnap instant"
        ]
        
        objective_text = "Votre objectif : retrouver votre tête tout en évitant de vous faire manger ou de finir dans une secte !"

        controls_text = "Contrôles : Utilisez les flèches directionnelles pour vous déplacer."

        content_width = screen_width - 100 * sfw
        content_height = screen_height - 400 * sfh

        content_surface = pg.Surface((content_width, content_height), pg.SRCALPHA)
        content_surface.fill((255, 255, 255, 160))

        story_surfaces = [story_font.render(line, True, (0, 0, 0)) for line in story_text]
        story_positions = [
            (content_width // 2, 75 + i * (story_font_size + 20))
            for i in range(len(story_text))
        ]

        objective_font_size = int(50 * sfw)
        objective_font = pg.font.Font(None, objective_font_size)
        objective_surface = objective_font.render(objective_text, True, (255, 0, 0))
        objective_position = (content_width // 2, 100 + len(story_text) * (story_font_size + 20))

        controls_font_size = int(40 * sfw)
        controls_font = pg.font.Font(None, controls_font_size)
        controls_surface = controls_font.render(controls_text, True, (0, 0, 0))
        controls_position = (content_width // 2, content_height - 50)

        for surface, position in zip(story_surfaces, story_positions):
            rect = surface.get_rect(center=position)
            content_surface.blit(surface, rect)

        objective_rect = objective_surface.get_rect(center=objective_position)
        content_surface.blit(objective_surface, objective_rect)

        controls_rect = controls_surface.get_rect(center=controls_position)
        content_surface.blit(controls_surface, controls_rect)

        bouton_retour = Button(self.game, "Retour", (200 * sfw, 50 * sfh),
                            int(50 * sfw), (120 * sfw, 50 * sfh))

        while True:
            self.game.clock.tick(self.game.FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                bouton_retour.event(event)

            self.game.screen.blit(self.background, (0, 0))
            self.game.particules.update_particles()
            self.game.screen.blit(title_text, title_rect)

            content_rect = content_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            self.game.screen.blit(content_surface, content_rect)
            bouton_retour.draw()

            if bouton_retour.is_clicked:
                self.game.state.lower_state()
                self.fadein()
                return

            self.game.utils.get_fps()
            self.game.utils.update_mouse()
            pg.display.flip()

    def settings(self):
        self.fadein()

        screen_height = self.game.settings.HEIGHT
        screen_width = self.game.settings.WIDTH
        sfw = self.game.settings.SCALE_FACTOR_WIDTH
        sfh = self.game.settings.SCALE_FACTOR_HEIGHT
        
        self.background = pg.transform.scale(self._background, (1920*sfw, 1080*sfh))

        menu_font_size = int(40 * sfw)
        menu_font = pg.font.Font(None, menu_font_size)
        menu_text = menu_font.render("Paramètres", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(screen_width // 2, screen_height // 10))

        button_height = int(100 * sfw)
        spacing = int(50 * sfw)

        bouton_son = Button(self.game, "Audio", (500 * sfw, button_height), 
                            int(100 * sfw), (screen_width // 2, screen_height // 2 - button_height + (spacing // 2)))
        
        bouton_graphismes = Button(self.game, "Résolution", (500 * sfw, button_height), 
                                   int(100 * sfw), (screen_width // 2, screen_height // 2 + button_height - (spacing // 2)))
        
        bouton_retour = Button(self.game, "Retour", (300 * sfw, button_height - 25), 
                               int(75 * sfw), (screen_width // 2, screen_height // 2 + (button_height + spacing) * 2))

        while True:
            self.game.clock.tick(self.game.FPS)
            self.game.screen.fill((0, 0, 0))
            self.game.screen.blit(self.background, (0, 0))
            self.game.screen.blit(menu_text, menu_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                bouton_son.event(event)
                bouton_graphismes.event(event)
                bouton_retour.event(event)

            self.game.particules.update_particles()
            bouton_son.draw()
            bouton_graphismes.draw()
            bouton_retour.draw()

            if bouton_son.is_clicked:
                self.game.state.modify_state("audio_menu")
                return
            if bouton_graphismes.is_clicked:
                self.game.state.modify_state("resolution_menu")
                return
            if bouton_retour.is_clicked:
                self.game.state.lower_state()
                self.fadein()
                return

            self.game.utils.get_fps()
            self.game.utils.update_mouse()
            pg.display.flip()
    
    def audio(self):
        self.fadein()

        sfw = self.game.settings.SCALE_FACTOR_WIDTH
        sfh = self.game.settings.SCALE_FACTOR_HEIGHT

        menu_font_size = int(40 * sfw)
        menu_font = pg.font.Font(None, menu_font_size)
        menu_text = menu_font.render("Audio", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(self.game.settings.WIDTH // 2, self.game.settings.HEIGHT // 10))
        slider_width, slider_height = int(500 * sfw), int(50 * sfh)
        button_height = int(75 * sfw)
        button_width = int(25 * sfw)
        spacing = int(50 * sfw)

        bouton_retour = Button(self.game, "Retour", (400 * sfw, button_height), 
                               int(50 * sfw), (self.game.settings.WIDTH // 2 - 300 * sfw, self.game.settings.HEIGHT // 2 + (button_height + spacing) * 2))
        
        bouton_sauvegarder = Button(self.game, "Sauvegarder", (400 * sfw, button_height),
                                    int(50 * sfw), (self.game.settings.WIDTH // 2 + 300 * sfw, 
                                                                   self.game.settings.HEIGHT // 2 + (button_height + spacing) * 2))

        confirm_bandeau = Bandeau(self.game, "Les paramètres ont bien été enregistrés !",
                                (500 * sfw, 70 * sfh),
                                int(30 * sfw), ((self.game.settings.WIDTH - 500 * sfw) // 2, 30 * sfh), (135, 206, 235), 2000)

        slider_volume_music = Slider(self.game.screen, (
        self.game.settings.WIDTH // 2, self.game.settings.HEIGHT // 3), slider_width, slider_height,
                                    button_width, 100, int(self.game.settings.music_volume * 100))
        slider_volume_effect = Slider(self.game.screen, (
        self.game.settings.WIDTH // 2, 2 * self.game.settings.HEIGHT // 3 - 150), slider_width, slider_height,
                                    button_width, 100, int(self.game.settings.effect_volume * 100))

        while True:
            self.game.clock.tick(self.game.FPS)
            self.game.screen.fill((0, 0, 0))
            self.game.screen.blit(menu_text,menu_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                slider_volume_effect.event(event)
                slider_volume_music.event(event)
                bouton_retour.event(event)
                bouton_sauvegarder.event(event)
                confirm_bandeau.update()

            self.game.particules.update_particles()
            slider_volume_music.draw()
            slider_volume_effect.draw()
            confirm_bandeau.draw()
            bouton_sauvegarder.draw()
            bouton_retour.draw()

            music_volume = slider_volume_music.slider_value
            effect_volume = slider_volume_effect.slider_value

            font_size = int(36 * sfw)
            font = pg.font.Font(None, font_size)
            music_text = font.render(f"Musique : {music_volume} %", True, (255, 255, 255))
            effect_text = font.render(f"Effets : {effect_volume} %", True, (255, 255, 255))

            music_rect = music_text.get_rect(topleft=(slider_volume_music.rect_x + slider_width + int(20 * sfw), slider_volume_music.rect_y))
            effect_rect = effect_text.get_rect(topleft=(slider_volume_effect.rect_x + slider_width + int(20 * sfw), slider_volume_effect.rect_y))

            self.game.screen.blit(music_text, music_rect)
            self.game.screen.blit(effect_text, effect_rect)

            if bouton_retour.is_clicked:
                self.game.state.lower_state()
                return
            if bouton_sauvegarder.is_clicked:
                confirm_bandeau.visible = True
                confirm_bandeau.creation_time = pg.time.get_ticks()
                self.game.settings.effect_volume = slider_volume_effect.slider_value / 100
                self.game.settings.music_volume = slider_volume_music.slider_value / 100
                self.game.settings.update_settings()
                self.game.utils.save_settings()
                bouton_sauvegarder.is_clicked = False

            self.game.utils.update_mouse()
            self.game.utils.get_fps()
            pg.display.flip()
    
    def resolution(self):
        self.fadein()

        screen_height = self.game.settings.HEIGHT
        screen_width = self.game.settings.WIDTH
        sfw = self.game.settings.SCALE_FACTOR_WIDTH
        sfh = self.game.settings.SCALE_FACTOR_HEIGHT

        menu_font_size = int(40 * sfw)
        menu_font = pg.font.Font(None, menu_font_size)
        menu_text = menu_font.render("Choix résolution", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(screen_width // 2, screen_height // 10))
        resolution_actuelle = pg.font.Font(None, int(50 * sfw)).render(f"Résolution actuelle : {self.game.settings.WIDTH}x{self.game.settings.HEIGHT}", True, (255, 255, 255))

        width_textzone = TextZone(self.game, "Largeur", (200 * sfw, 50 * sfh), 
                                  int(50 * sfw), (screen_width // 2 - 200 * sfw, screen_height // 2) , 4, [int])
        
        height_textzone = TextZone(self.game, "Hauteur", (200 * sfw, 50 * sfh), 
                                   int(50 * sfw), (screen_width // 2 + 200 * sfw, screen_height // 2), 4, [int])
        
        valider_button = Button(self.game, "Valider", (200 * sfw, 50 * sfh), 
                                int(50 * sfw), (screen_width // 2, screen_height // 1.5 + 100 * sfh))

        bouton_retour = Button(self.game, "Retour", (200 * sfw, 35 * sfh), 
                               int(50 * sfw), (120 * sfw, 50 * sfh))

        erreur_bandeau = Bandeau(self.game, "Vous devez entrer une résolution valide!", (500 * sfw, 70 * sfh), 
                                 int(30 * sfw), ((self.game.settings.WIDTH - 500 * sfw) // 2, 30 * sfh), (255, 0, 0, 150), 2000)

        while True:
            self.game.clock.tick(self.game.FPS)
            self.game.screen.fill((0, 0, 0))
            self.game.screen.blit(menu_text, menu_rect)
            self.game.screen.blit(resolution_actuelle, resolution_actuelle.get_rect(center=(screen_width // 2, screen_height // 3 * sfh)))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                height_textzone.event(event)
                width_textzone.event(event)
                bouton_retour.event(event)
                valider_button.event(event)
                erreur_bandeau.update()
            
            self.game.particules.update_particles()
            height_textzone.draw()
            bouton_retour.draw()
            width_textzone.draw()
            valider_button.draw()
            erreur_bandeau.draw()

            if valider_button.is_clicked:
                if height_textzone.get() and width_textzone.get():
                        resolution = (int(width_textzone.get()), int(height_textzone.get()))
                        if resolution[0] < 1200:
                            resolution = (1200, resolution[1])
                        if resolution[1] < 800:
                            resolution = (resolution[0], 800)
                        if resolution[0] > self.game.settings.originalWidth:
                            resolution = (self.game.settings.originalWidth, resolution[1])
                        if resolution[1] > self.game.settings.originalHeight:
                            resolution = (resolution[0], self.game.settings.originalHeight)
                        if resolution == (self.game.settings.originalWidth, self.game.settings.originalHeight):
                            self.game.settings.WIDTH, self.game.settings.HEIGHT = resolution
                            self.game.settings.SCALE_FACTOR_WIDTH = self.game.settings.WIDTH / self.game.settings.originalWidth
                            self.game.settings.SCALE_FACTOR_HEIGHT = self.game.settings.HEIGHT / self.game.settings.originalHeight
                            self.game.screen = pg.display.set_mode((self.game.settings.WIDTH, self.game.settings.HEIGHT), pg.FULLSCREEN)
                        else:
                            self.game.settings.WIDTH, self.game.settings.HEIGHT = resolution
                            self.game.settings.SCALE_FACTOR_WIDTH = self.game.settings.WIDTH / self.game.settings.originalWidth
                            self.game.settings.SCALE_FACTOR_HEIGHT = self.game.settings.HEIGHT / self.game.settings.originalHeight
                            self.game.screen = pg.display.set_mode((self.game.settings.WIDTH, self.game.settings.HEIGHT))
                        sr = pg.display.get_surface().get_rect()
                        self.game.menu.veil = pg.Surface(sr.size)
                        self.game.menu.veil.fill((0, 0, 0))
                        self.game.settings.WIDTH, self.game.settings.HEIGHT = resolution
                        self.game.settings.update_settings()
                        self.game.utils.save_settings()
                        return
                else:
                    self.game.utils.error_sound.play()
                    erreur_bandeau.visible = True
                    erreur_bandeau.creation_time = pg.time.get_ticks()
                    valider_button.is_clicked = False

            if bouton_retour.is_clicked:
                self.game.state.lower_state()
                return

            self.game.utils.get_fps()
            self.game.utils.update_mouse()
            pg.display.flip()
