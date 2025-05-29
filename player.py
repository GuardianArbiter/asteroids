import pygame
from constants import *
from circleshape import CircleShape
from shots import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self,screen):
        shape = self.triangle()
        color = (255, 255, 255)
        pygame.draw.polygon(screen,color, shape, 2)

    def rotate(self,dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        print(dt)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        negative_dt = dt * -1
        if keys[pygame.K_a]:
            self.rotate(negative_dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(negative_dt)
        if keys[pygame.K_SPACE]:
            self.shoot() 
        self.timer -= dt       

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt


    def shoot(self):
        if self.timer > 0:
            pass
        else:
            new_shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            base_direction = pygame.Vector2(0,1)
            shot_direction = base_direction.rotate(self.rotation)
            new_shot.velocity = shot_direction * PLAYER_SHOOT_SPEED
            self.timer = PLAYER_SHOOT_COOLDOWN

        