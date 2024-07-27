import random
from random import randint

import pygame

from constants import WIDTH, HEIGHT
from coin import Coin


class Platform(pygame.sprite.Sprite):
    """ Class for the platforms on which the player moves. Each platform has an equal 33% chance to be stationary, move
    to the left, or move to the right. Stationary platforms have a 1 in 6 chance to generate with a coin. """

    def __init__(self, width: int = 0, height: int = 18, difficulty=0, prev_height=None):
        super().__init__()

        if width == 0:
            width = random.randint(50, 120)

        scaling = max(1 - (difficulty / 100), 0.2)
        width *= scaling
        height_coordinate = prev_height - random.randint(70, 80 + difficulty) if prev_height\
            else random.randint(0, HEIGHT - 30)

        self.image = pygame.image.load("data/platform.png")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10), height_coordinate))
        self.point = True  # When the player passes each platform this is set to False and 0.1 is added to score
        self.speed = random.randint(-1, 1)  # -1 Moves to the left, 0 is stationary, 1 moves to the right
        self.moving = True
        self.crumbles = random.randint(1, 100) < min(difficulty, 90)
        self.n_cracks = 0
        self.last_crack_time = None
        self.base_platform = False
        self.coin = None

    def move(self, player):
        hits = self.rect.colliderect(player.rect)
        if self.moving:
            self.rect.move_ip(self.speed, 0)
            if hits:
                player.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
                if self.coin:
                    self.coin.rect.centerx = self.rect.centerx
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH
                if self.coin:
                    self.coin.rect.centerx = self.rect.centerx

    def generate_coin(self, all_coins):
        dice_roll = randint(1, 6)
        if dice_roll == 6:
            new_coin = Coin((self.rect.centerx, self.rect.centery - 30), speed=self.speed)
            all_coins.add(new_coin)
            self.coin = new_coin

    def check_crumble(self, player):
        if not self.crumbles:
            return None

        hits = self.rect.colliderect(player.rect)
        now = pygame.time.get_ticks()
        if hits and player.vel.y == 0.5 and self.n_cracks == 0:
            self.image = pygame.image.load("data/platform_cracked_1.png")
            self.surf = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            self.last_crack_time = now
            self.n_cracks += 1

        if self.n_cracks == 1 and now - self.last_crack_time > 1000:
            self.image = pygame.image.load("data/platform_cracked_2.png")
            self.surf = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            self.last_crack_time = now
            self.n_cracks += 1

        if self.n_cracks == 2 and now - self.last_crack_time > 1000:
            self.image = pygame.image.load("data/platform_cracked_3.png")
            self.surf = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            self.last_crack_time = now
            self.n_cracks += 1

        if self.n_cracks == 3 and now - self.last_crack_time > 1000:
            self.kill()
