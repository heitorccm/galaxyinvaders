import pygame
from PPlay.sprite import Sprite

class Nave:
    def __init__(self, x1, y1, speed):
        self.surface_descendo = pygame.image.load(r"assets\nave2.png").convert_alpha()
        self.surface_subindo = pygame.image.load(r"assets\nave1.png").convert_alpha()
        self.sprite = Sprite(r"assets\nave2.png")
        self.sprite.image = self.surface_descendo
        self.sprite.set_position(x1, y1)
        self.speed = speed
    def move_down(self, delta_time):
        self.sprite.image = self.surface_descendo
        self.sprite.y += self.speed * delta_time
    def move_up(self, delta_time):
        self.sprite.image = self.surface_subindo
        self.sprite.y -= self.speed * delta_time
    def lock1(self):
        self.sprite.image = self.surface_subindo
        self.sprite.y = 610
    def lock2(self):
        self.sprite.image = self.surface_subindo
        self.sprite.y = -50
    def draw(self):
        self.sprite.draw()