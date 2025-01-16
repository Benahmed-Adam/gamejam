import pygame as pg
from pygame.locals import *
import random
import json
import math
import os
import sys

class Settings:
    def __init__(self,game):
        self.game = game
        self.originalWidth = pg.display.Info().current_w
        self.originalHeight = pg.display.Info().current_h
        self.WIDTH, self.HEIGHT = game.utils.settings_data["resolution"]
        self.SCALE_FACTOR_WIDTH = self.WIDTH / 1920
        self.SCALE_FACTOR_HEIGHT = self.HEIGHT / 1080
        self.music_volume = game.utils.settings_data["musique"]
        self.effect_volume = game.utils.settings_data["effects"]
        if self.WIDTH > self.originalWidth:
            self.WIDTH = self.originalWidth
            self.update_settings()
            self.game.utils.save_settings()
        if self.HEIGHT > self.originalHeight:
            self.HEIGHT = self.originalHeight
            self.update_settings()
            self.game.utils.save_settings()
        if self.WIDTH != self.originalWidth or self.HEIGHT != self.originalHeight:
            self.game.screen = pg.display.set_mode((self.WIDTH,self.HEIGHT))
        else:
            self.game.screen = pg.display.set_mode((self.WIDTH,self.HEIGHT),pg.FULLSCREEN)


    def update_settings(self):
        self.game.utils.settings_data["musique"] = self.music_volume
        self.game.utils.settings_data["effects"] = self.effect_volume
        self.game.utils.settings_data["resolution"] = [self.WIDTH,self.HEIGHT]
        self.game.utils.menu_sound.set_volume(self.music_volume)
        self.game.utils.effect_button_sound.set_volume(self.effect_volume)
        self.game.utils.error_sound.set_volume(self.effect_volume)
        self.game.utils.game_sound.set_volume(self.music_volume)
        self.game.utils.win_sound.set_volume(self.music_volume)
        self.game.utils.loose_chevalier_sound.set_volume(self.music_volume)
        self.game.utils.loose_pirate_sound.set_volume(self.music_volume)
        self.SCALE_FACTOR_WIDTH = self.WIDTH / 1920
        self.SCALE_FACTOR_HEIGHT = self.HEIGHT / 1080
