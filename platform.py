import random
from random import randint

import pygame

from constants import WIDTH, HEIGHT
from coin import Coin


class Platform(pygame.sprite.Sprite):
    def __init__(self, width = 0, height = 18):
        super().__init__()

        if width == 0:
            width = random.randint(50, 120)

        self.image = pygame.image.load("data/platform.png")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                               random.randint(0, HEIGHT - 30)))
        self.point = True
        self.speed = random.randint(-1, 1)
        self.moving = True

    def move(self, player):
        hits = self.rect.colliderect(player.rect)
        if self.moving:
            self.rect.move_ip(self.speed, 0)
            if hits:
                player.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

    def generate_coin(self, all_coins):
        dice_roll = randint(1, 6)
        if (self.speed == 0) and dice_roll == 6:
            all_coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))
