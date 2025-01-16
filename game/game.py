from utils.settings import *
from .ui import Button

class Entity:
    def __init__(self, size: tuple, position: pg.Vector2, tex_path="ressources/chicken.png", game=None):
        self.game = game
        self.size = (int(size[0] * self.game.settings.SCALE_FACTOR_WIDTH), 
                     int(size[1] * self.game.settings.SCALE_FACTOR_HEIGHT))
        self.position = pg.Vector2(position.x * self.game.settings.SCALE_FACTOR_WIDTH,
                                    position.y * self.game.settings.SCALE_FACTOR_HEIGHT)
        self.texture = pg.transform.scale(pg.image.load(tex_path), self.size).convert_alpha()
        self.font = pg.font.Font(None, int(40 * self.game.settings.SCALE_FACTOR_HEIGHT))
        self.time = 5000
        self.creation_time = pg.time.get_ticks()
        self.speed = 6 * self.game.settings.SCALE_FACTOR_WIDTH
        self.health = 10
        self.damages = 1
        self.alive = True
    
    def draw(self, screen: pg.Surface):
        screen.blit(self.texture, self.position)
    
    def move(self, player_pos: pg.Vector2):
        direction = player_pos - self.position
        if direction.length() > 0:
            direction = direction.normalize() * self.speed
        self.position += direction
    
    def update(self):
        if self.health <= 0:
            self.alive = False


class Bomb(Entity):
    def __init__(self, size, position, tex_path="ressources/bomb.png", game=None):
        super().__init__(size, position, tex_path, game)
        self.radius = random.randint(100, 300) * self.game.settings.SCALE_FACTOR_WIDTH
        self.damages = random.randint(50, 200)
    
    def draw(self, screen: pg.Surface):
        texture_center_pos = self.position - pg.Vector2(self.size[0] / 2, self.size[1] / 2)
        screen.blit(self.texture, texture_center_pos)

        circle_surface = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        pg.draw.circle(circle_surface, (255, 0, 0, 75), (self.radius, self.radius), self.radius)
        screen.blit(circle_surface, (self.position.x - self.radius, self.position.y - self.radius))

        current_time = pg.time.get_ticks()
        remaining_time = max(0, (self.time - (current_time - self.creation_time)) // 1000) + 1

        timer_text = self.font.render(str(remaining_time), True, (255, 255, 255))
        text_rect = timer_text.get_rect(center=(self.position.x, self.position.y - self.size[1] // 2 - 20))
        screen.blit(timer_text, text_rect)

    def update(self):
        current_time = pg.time.get_ticks()
        if current_time - self.creation_time >= self.time:
            self.alive = False

class Shield(Entity):
    def __init__(self, size, position, tex_path="ressources/shield.png", game=None):
        super().__init__(size, position, tex_path, game)
        self.health = 50
        self.damages = 1

class DamagesBoost(Entity):
    def __init__(self, size, position, tex_path="ressources/sword.png", game=None):
        super().__init__(size, position, tex_path, game)
        self.health = 1
        self.damages = 10

class Morceau_de_tete(Entity):
    def __init__(self, size, position, tex_path="ressources/morceau_tete.png", game=None):
        super().__init__(size, position, tex_path, game)

class Pirate(Entity):
    def __init__(self, size, position, tex_path="ressources/pirate.png", game=None):
        super().__init__(size, position, tex_path, game)
        self.speed = 7 * self.game.settings.SCALE_FACTOR_WIDTH
        self.health = 75
        self.damages = 5

    def draw(self, screen: pg.Surface):
        screen.blit(self.texture, self.position)
        text = self.font.render(f"{self.health}/75", True, (255, 255, 255))
        rect = text.get_rect(midbottom=(self.position.x + self.texture.get_size()[0] // 2, self.position.y))
        screen.blit(text, rect)
    
class Chevalier(Entity):
    def __init__(self, size, position, tex_path="ressources/chevalier.png", game=None):
        super().__init__(size, position, tex_path, game)
        self.speed = 3 * self.game.settings.SCALE_FACTOR_WIDTH
        self.health = 250
        self.damages = 2

    def draw(self, screen: pg.Surface):
        screen.blit(self.texture, self.position)
        text = self.font.render(f"{self.health}/250", True, (255, 255, 255))
        rect = text.get_rect(midbottom=(self.position.x + self.texture.get_size()[0] // 2, self.position.y))
        screen.blit(text, rect)
    
    def move(self, player_pos: pg.Vector2, pirates: list[Pirate]):
        direction = player_pos - self.position
        self.speed = 3 * self.game.settings.SCALE_FACTOR_WIDTH
        if direction.length() > 0:
            direction = direction.normalize() * self.speed
        for p in pirates:
            distance = self.position.distance_to(p.position)
            if distance < 500 * self.game.settings.SCALE_FACTOR_WIDTH:
                self.speed = 10 * self.game.settings.SCALE_FACTOR_WIDTH
                direction = p.position - self.position
                if direction.length() > 0:
                    direction = direction.normalize() * self.speed

        self.position += direction

class Poulet(Entity):
    def __init__(self, size, position, tex_path="ressources/chicken.png", game=None):
        super().__init__(size, position, tex_path, game)
        self.nb_morceaux = 0
    
    def update(self):
        if self.health <= 0:
            self.alive = False

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.position.x -= 10 * self.game.settings.SCALE_FACTOR_WIDTH
        if keys[pg.K_RIGHT]:
            self.position.x += 10 * self.game.settings.SCALE_FACTOR_WIDTH
        if keys[pg.K_UP]:
            self.position.y -= 10 * self.game.settings.SCALE_FACTOR_HEIGHT
        if keys[pg.K_DOWN]:
            self.position.y += 10 * self.game.settings.SCALE_FACTOR_HEIGHT

        self.position.x %= 1920 * self.game.settings.SCALE_FACTOR_WIDTH
        self.position.y %= 1080 * self.game.settings.SCALE_FACTOR_HEIGHT

    def draw(self, screen: pg.Surface):
        screen.blit(self.texture, self.position)
        rect_width, rect_height = int(400 * self.game.settings.SCALE_FACTOR_WIDTH), int(150 * self.game.settings.SCALE_FACTOR_HEIGHT)
        rect_x = screen.get_width() // 2 - rect_width // 2
        rect_y = int(10 * self.game.settings.SCALE_FACTOR_HEIGHT)

        surf = pg.Surface((rect_width, rect_height), pg.SRCALPHA)
        pg.draw.rect(surf, (0, 0, 255, 128), pg.Rect(0, 0, rect_width, rect_height), border_radius=10)

        font = pg.font.Font(None, int(30 * self.game.settings.SCALE_FACTOR_HEIGHT))

        health_text = font.render(f"Santé: {self.health}", True, (255, 255, 255))
        damages_text = font.render(f"Dégâts: {self.damages}", True, (255, 255, 255))
        morceaux_text = font.render(f"Morceaux de tête: {self.nb_morceaux}/5", True, (255, 255, 255))

        text_spacing = int(10 * self.game.settings.SCALE_FACTOR_HEIGHT)
        start_y = (rect_height - (health_text.get_height() * 3 + text_spacing * 2)) // 2

        surf.blit(health_text, (int(10 * self.game.settings.SCALE_FACTOR_WIDTH), start_y))
        surf.blit(damages_text, (int(10 * self.game.settings.SCALE_FACTOR_WIDTH), start_y + health_text.get_height() + text_spacing))
        surf.blit(morceaux_text, (int(10 * self.game.settings.SCALE_FACTOR_WIDTH), start_y + (health_text.get_height() + text_spacing) * 2))

        screen.blit(surf, (rect_x, rect_y))

class Chepa:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.running = True
        sr = pg.display.get_surface().get_rect()
        self.veil = pg.Surface(sr.size)
        self.veil.fill((0, 0, 0))
        self.pirates: list[Pirate] = []
        self.chevaliers: list[Chevalier] = []
        self.boosts = [random.choice([Shield((75, 75), pg.Vector2(random.randint(150, 1700), random.randint(150, 820)), game=self.game), DamagesBoost((75, 75), pg.Vector2(random.randint(100, 1820), random.randint(100, 880)), game=self.game)]) for _ in range(random.randint(1, 5))]
        self.player = Poulet((100, 100), pg.Vector2(self.game.settings.WIDTH//2, self.game.settings.HEIGHT//2), game=self.game)
        self.morceaux: list[Morceau_de_tete] = []
        self.bombs: list[Bomb] = []
        self.boom = pg.mixer.Sound("ressources/boom.mp3")
        self.boom.set_volume(self.game.settings.effect_volume)
        self.scream = pg.mixer.Sound("ressources/scream.mp3")
        self.scream.set_volume(self.game.settings.effect_volume)
        self.success = pg.mixer.Sound("ressources/success.mp3")
        self.success.set_volume(self.game.settings.effect_volume)
        self.sword = pg.mixer.Sound("ressources/sword.mp3")
        self.sword.set_volume(self.game.settings.effect_volume)
        self.shield = pg.mixer.Sound("ressources/shield.mp3")
        self.shield.set_volume(self.game.settings.effect_volume)

    
    def reset(self):
        self.running = True
        sr = pg.display.get_surface().get_rect()
        self.veil = pg.Surface(sr.size)
        self.veil.fill((0, 0, 0))
        self.pirates: list[Pirate] = []
        self.chevaliers: list[Chevalier] = []
        self.boosts = [random.choice([Shield((75, 75), pg.Vector2(random.randint(150, 1700), random.randint(150, 820)), game=self.game), DamagesBoost((75, 75), pg.Vector2(random.randint(100, 1820), random.randint(100, 880)),game=self.game)]) for _ in range(random.randint(1, 5))]
        self.player = Poulet((100, 100), pg.Vector2(self.game.settings.WIDTH//2, self.game.settings.HEIGHT//2), game=self.game)
        self.morceaux: list[Morceau_de_tete] = []
        self.bombs: list[Bomb] = []

    def update(self):
        self.player.update()
        if not self.player.alive:
            self.loose("p")
            self.running = False
        if self.player.nb_morceaux >= 5:
            self.game.state.modify_state("win")
            self.running = False
        entities = self.pirates + self.chevaliers + [self.player] + self.boosts + self.morceaux + self.bombs
        for i, entity1 in enumerate(entities):
            for j, entity2 in enumerate(entities):
                if i != j and self.check_collision(entity1, entity2):
                    self.resolve_collision(entity1, entity2)
        for p in self.pirates:
            p.update()
            p.move(self.player.position)
            if not p.alive:
                n = random.randint(0, 100)
                if n <= 20:
                    if (self.player.nb_morceaux + len(self.morceaux) <= 4):
                        self.morceaux.append(Morceau_de_tete((100, 100), pg.Vector2(p.position.x, p.position.y), game=self.game))
                self.scream.play()
                self.pirates.remove(p)
        for c in self.chevaliers:
            c.update()
            c.move(self.player.position, self.pirates)
            if not c.alive:
                self.boosts.append(random.choice([Shield((75, 75), c.position, game=self.game), DamagesBoost((75, 75), c.position, game=self.game)]))
                self.scream.play()
                self.chevaliers.remove(c)
        for b in self.bombs:
            b.update()
            if not b.alive:
                for e in entities:
                    distance = b.position.distance_to(e.position)
                    if distance < b.radius:
                        e.health -= b.damages
                self.boom.play()
                self.bombs.remove(b)
        if len(self.pirates) <= 1:
            if random.randint(0, 200) == 1:
                nb = random.randint(1, 5)
                for i in range(nb):
                    self.pirates.append(Pirate((100, 100), pg.Vector2(2000, random.randint(0, 1080)), game=self.game))
        if len(self.chevaliers) <= 1:
            if random.randint(0, 200) == 1:
                nb = random.randint(1, 5)
                for i in range(nb):
                    self.chevaliers.append(Chevalier((100, 100), pg.Vector2(-100, random.randint(0, 1080)), game=self.game))
        if len(self.bombs) <= 1:
            if random.randint(0, 250) == 1:
                self.bombs.append(Bomb((75, 75), pg.Vector2(random.randint(150, 1700), random.randint(150, 820)), game=self.game))

    def check_collision(self, entity1: Entity, entity2: Entity):
        rect1 = pg.Rect(entity1.position.x, entity1.position.y, *entity1.size)
        rect2 = pg.Rect(entity2.position.x, entity2.position.y, *entity2.size)
        return rect1.colliderect(rect2)

    def resolve_collision(self, entity1: Entity, entity2: Entity):
        collision_direction = entity2.position - entity1.position
        if collision_direction.length() > 0:
            collision_direction = collision_direction.normalize()
            entity1.position -= collision_direction * entity1.speed * 0.5
            entity2.position += collision_direction * entity2.speed * 0.5

        if (isinstance(entity1, Poulet) and isinstance(entity2, Chevalier)) or isinstance(entity1, Chevalier) and isinstance(entity2, Poulet):
            self.player.health = -1
            self.loose("c")
            self.running = False
        elif (isinstance(entity1, Poulet) and isinstance(entity2, Pirate)) or isinstance(entity1, Pirate) and isinstance(entity2, Poulet):
            entity1.health -= entity2.damages
            entity2.health -= entity1.damages
        elif (isinstance(entity1, Pirate) and isinstance(entity2, Chevalier)) or (isinstance(entity1, Chevalier) and isinstance(entity2, Pirate)):
            entity1.health -= entity2.damages
            entity2.health -= entity1.damages
        elif (isinstance(entity1, Poulet) and isinstance(entity2, Shield)):
            entity1.health += entity2.health
            entity1.damages += entity2.damages
            self.boosts.remove(entity2)
            self.shield.play()
        elif (isinstance(entity1, Poulet) and isinstance(entity2, DamagesBoost)):
            entity1.health += entity2.health
            entity1.damages += entity2.damages
            self.boosts.remove(entity2)
            self.sword.play()
        elif (isinstance(entity1, Poulet) and isinstance(entity2, Morceau_de_tete)):
            self.morceaux.remove(entity2)
            self.player.nb_morceaux += 1
            self.success.play()

    def draw(self):
        self.screen.blit(self.bg, (0,0))
        for p in self.pirates:
            p.draw(self.screen)
        for b in self.boosts:
            b.draw(self.screen)
        for c in self.chevaliers:
            c.draw(self.screen)
        for m in self.morceaux:
            m.draw(self.screen)
        for b in self.bombs:
            b.draw(self.screen)
        self.player.draw(self.screen)
        self.game.utils.get_fps()
    
    def pause_menu(self):
        screen_height = self.game.settings.HEIGHT
        screen_width = self.game.settings.WIDTH
        scale_factor_width = self.game.settings.SCALE_FACTOR_WIDTH
        scale_factor_height = self.game.settings.SCALE_FACTOR_HEIGHT

        button_quit = Button(self.game, "Quitter", (500 * scale_factor_width, 100*scale_factor_height), 
                             int(75 * scale_factor_width), (screen_width//2, screen_height//2))
        
        button_resume = Button(self.game, "Reprendre", (500 * scale_factor_width, 100*scale_factor_height), 
                               int(75 * scale_factor_width), (screen_width//2, screen_height//3))

        while True:
            self.game.clock.tick(self.game.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return
                button_quit.event(event)
                button_resume.event(event)
            if button_quit.is_clicked:
                self.running = False
                self.game.state.lower_state()
                return
            if button_resume.is_clicked:
                return
            self.draw()
            self.veil.set_alpha(220)
            self.game.screen.blit(self.veil, (0, 0))
            button_quit.draw()
            button_resume.draw()
            self.game.utils.update_mouse()
            pg.display.flip()
    
    def win(self):
        screen_height = self.game.settings.HEIGHT
        screen_width = self.game.settings.WIDTH
        scale_factor_width = self.game.settings.SCALE_FACTOR_WIDTH
        scale_factor_height = self.game.settings.SCALE_FACTOR_HEIGHT

        button_resume = Button(self.game, "Rejouer", (500 * scale_factor_width, 100*scale_factor_height), 
                            int(75 * scale_factor_width), (screen_width//2, screen_height//2))

        font = pg.font.SysFont(None, 50)
        text_surface = font.render("Tu as retrouvé ta tête, toutes mes felicitations !", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(screen_width//2, screen_height//4))
        bg = pg.transform.scale(pg.image.load("ressources/win_bg.jpg"), (1920*scale_factor_width, 1080*scale_factor_width))

        while True:
            self.game.clock.tick(self.game.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return
                button_resume.event(event)

            if button_resume.is_clicked:
                self.reset()
                self.game.state.lower_state()
                return

            self.draw()
            self.game.screen.blit(bg, (0, 0))
            self.veil.set_alpha(120)
            self.game.screen.blit(self.veil, (0, 0))

            self.game.screen.blit(text_surface, text_rect)
            button_resume.draw()

            self.game.utils.update_mouse()
            pg.display.flip()
    
    def loose(self, en: str):
        if en == "c":
            self.message = "Tu as fini dans une secte"
            self.ending_background = pg.image.load("ressources/chevalierending.jpg")
            self.game.state.modify_state("loose_chevalier")
        else:
            self.message = "Tu as fini en brochettes (t mort)"
            self.ending_background = pg.image.load("ressources/pirateending.jpg")
            self.game.state.modify_state("loose_pirate")
        

    def loose_message(self):
        screen_height = self.game.settings.HEIGHT
        screen_width = self.game.settings.WIDTH
        scale_factor_width = self.game.settings.SCALE_FACTOR_WIDTH
        scale_factor_height = self.game.settings.SCALE_FACTOR_HEIGHT
        
        self.ending_background = pg.transform.scale(self.ending_background, (1920*scale_factor_width, 1080*scale_factor_width))

        button_resume = Button(self.game, "Réessayer", (500 * scale_factor_width, 100*scale_factor_height), 
                            int(75 * scale_factor_width), (screen_width//2, screen_height//2))

        font = pg.font.SysFont(None, 50)
        text_surface = font.render(self.message, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(screen_width//2, screen_height//4))

        while True:
            self.game.clock.tick(self.game.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return
                button_resume.event(event)

            if button_resume.is_clicked:
                self.reset()
                self.game.state.lower_state()
                return

            self.draw()
            self.game.screen.blit(self.ending_background, (0, 0))
            self.veil.set_alpha(120)
            self.game.screen.blit(self.veil, (0, 0))

            self.game.screen.blit(text_surface, text_rect)
            button_resume.draw()

            self.game.utils.update_mouse()
            pg.display.flip()

    def play(self):
        self.bg = pg.transform.scale(pg.image.load("ressources/ground.jpg"), (1920*self.game.settings.SCALE_FACTOR_WIDTH, 1080*self.game.settings.SCALE_FACTOR_HEIGHT)).convert_alpha()
        while self.running:
            self.game.clock.tick(self.game.FPS)
            self.update()
            self.draw()
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.pause_menu()
        self.running = True