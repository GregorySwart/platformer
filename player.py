import pygame
from pygame.locals import K_LEFT, K_RIGHT

from constants import WIDTH, ACC, FRIC

vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("data/character.png")
        self.rect = self.surf.get_rect(center=(10, 420))

        self.pos = vec((10, 385))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.score = 0
        self.touching_platform = False

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x += -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x += ACC

        if not pressed_keys[K_LEFT] and not pressed_keys[K_RIGHT] and self.touching_platform:
            self.acc.x += self.vel.x * FRIC * 2  # Make player slide around less on platforms
        else:
            self.acc.x += self.vel.x * FRIC

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def update(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.touching_platform = True if hits else False

        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point:
                        hits[0].point = False
                        self.score += 1
                    self.jumping = False
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0

    def jump(self):
        if self.touching_platform and not self.jumping:
            self.jumping = True
            self.vel.y = -17

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
