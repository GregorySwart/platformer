import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_LSHIFT, K_SPACE

from constants import WIDTH, ACC, FRIC

vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    """ Class for the player """
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

        self.already_strafed = False
        self.already_double_jumped = False

    def move(self, events):
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

        # Strafing
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == K_LSHIFT:
                if not pressed_keys[K_SPACE] or self.vel.y > -8:  # This -8 figure could be further tweaked
                    if not self.touching_platform and not self.already_strafed:
                        if pressed_keys[K_LEFT]:
                            self.vel.x -= 9
                            self.vel.y -= 4
                        elif pressed_keys[K_RIGHT]:
                            self.vel.x += 9
                            self.vel.y -= 4
                        self.already_strafed = True

        # Double jump
        if not self.touching_platform:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == K_SPACE and not self.already_double_jumped:
                    self.vel.y -= 10
                    self.already_double_jumped = True

        if self.touching_platform and self.vel.y == 0.5:  # y velocity seems to be 0.5 when resting on a platform
            self.already_strafed = False
            self.already_double_jumped = False

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
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    # def strafe(self, left=True):
    #     if self.prep_strafe_left:
    #         self.prep_strafe_left = False
    #         self.vel.x -= 10
    #     else:
    #         self.prep_strafe_right = False
    #         self.vel.x += 10
