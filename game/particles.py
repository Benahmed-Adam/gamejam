from utils.settings import *

class Particules:
    def __init__(self, game):
        self.game = game
        self.particles = []
        self.last_spawn_time = 0
        self.spawn_interval = 50

    def create_particle(self):
        x = random.uniform(20, self.game.settings.WIDTH - 20)
        y = random.uniform(20, self.game.settings.HEIGHT - 20)
        velocity_x = random.uniform(-1.0, 1.0)
        velocity_y = random.uniform(-1.0, -0.5)
        size = random.randint(4, 15)
        lifespan = random.uniform(1.0, 3.0)
        return {"position": [x, y], "velocity": [velocity_x, velocity_y], "size": size, "lifespan": lifespan}

    def update_particles(self):
        current_time = pg.time.get_ticks()

        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.particles.append(self.create_particle())
            self.last_spawn_time = current_time

        for particle in self.particles[:]:
            particle["position"][0] += particle["velocity"][0]
            particle["position"][1] += particle["velocity"][1]
            particle["size"] -= 0.1
            particle["velocity"][1] += 0.02
            particle["lifespan"] -= 1 / self.game.FPS

            if particle["size"] > 0:
                self.draw_particle(particle)

            if particle["size"] <= 0 or particle["lifespan"] <= 0:
                self.particles.remove(particle)

    def draw_particle(self, particle):
        x, y = particle["position"]
        radius = int(particle["size"])
        pg.draw.circle(self.game.screen, (255, 255, 255), (int(x), int(y)), radius)

        glow_radius = radius * 2
        glow_surf = pg.Surface((glow_radius * 2, glow_radius * 2), pg.SRCALPHA)
        pg.draw.circle(glow_surf, (20, 20, 60, 100), (glow_radius, glow_radius), glow_radius)
        self.game.screen.blit(glow_surf, (int(x - glow_radius), int(y - glow_radius)), special_flags=pg.BLEND_RGB_ADD)
