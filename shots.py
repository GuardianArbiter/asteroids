import pygame
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self,screen):
        color = (255, 255, 255)
        pygame.draw.circle(screen, color, self.position, SHOT_RADIUS, 2)

    def update(self, dt):
        self.position += self.velocity * dt