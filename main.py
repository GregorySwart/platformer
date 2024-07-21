import pygame
import sys
from pygame.locals import *
import random
import time

from constants import HEIGHT, WIDTH, FPS
from platform import Platform
from player import Player

pygame.init()
vec = pygame.math.Vector2  # 2 for two-dimensional

FramePerSec = pygame.time.Clock()

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
background_image = pygame.image.load("data/background.png")
background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


def check_score():
    point_platforms = [p for p in platforms if p.point]
    for p in point_platforms:
        if player.rect.y < p.rect.y:
            player.score += 0.1
            p.point = False


def generate_platforms():
    while len(platforms) < 7:
        width = random.randrange(50,100)
        platforms_overlap = True

        while platforms_overlap:
            new_platforms = Platform()
            new_platforms.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            platforms_overlap = check_platform_overlap(new_platforms, platforms)

        new_platforms.generate_coin(coins)
        platforms.add(new_platforms)
        all_sprites.add(new_platforms)


def check_platform_overlap(new_platform, all_platforms):
    if pygame.sprite.spritecollideany(new_platform, all_platforms):
        return True
    else:
        for p in all_platforms:
            if p == new_platform:
                continue
            if (abs(new_platform.rect.top - p.rect.bottom) < 10) or (abs(new_platform.rect.bottom - p.rect.top) < 10):
                return True
        return False


# Initial platform
initial_platform = Platform(width=WIDTH)
initial_platform.rect = initial_platform.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
initial_platform.moving = False
initial_platform.point = False

# Initialise player
player = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(initial_platform)
all_sprites.add(player)

platforms = pygame.sprite.Group()
platforms.add(initial_platform)

coins = pygame.sprite.Group()

# Initial level generation
for x in range(random.randint(5, 6)):
    C = True
    pl = Platform()
    while C:
        pl = Platform()
        C = check_platform_overlap(pl, platforms)

    pl.generate_coin(coins)
    platforms.add(pl)
    all_sprites.add(pl)

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.cancel_jump()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if player.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
        time.sleep(1)
        display_surface.fill((255, 0, 0))
        pygame.display.update()
        time.sleep(1)
        pygame.quit()
        sys.exit()

    display_surface.blit(background, (0, 0))
    f = pygame.font.SysFont("Verdana", 20)
    g = f.render("Score:" + str(round(player.score)), True, (123, 255, 0))
    text_rect = g.get_rect(center=(WIDTH / 2, 20))
    display_surface.blit(g, text_rect)

    if player.rect.top <= HEIGHT / 3:
        player.pos.y += abs(player.vel.y)
        for plat in platforms:
            plat.rect.y += abs(player.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
        for coin in coins:
            coin.rect.y += abs(player.vel.y)
            if coin.rect.top >= HEIGHT:
                coin.kill()

    if len(platforms) < 7:
        generate_platforms()

    player.update(platforms=platforms)
    player.move()

    for entity in all_sprites:
        display_surface.blit(entity.surf, entity.rect)

    for plat in platforms:
        plat.move(player)

    for coin in coins:
        display_surface.blit(coin.image, coin.rect)
        coin.update(player)

    check_score()

    pygame.display.update()
    FramePerSec.tick(FPS)
