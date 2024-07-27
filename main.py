import pygame
import sys
from pygame.locals import *
import random
import time

from constants import HEIGHT, WIDTH, FPS, DEV_MODE
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


def generate_platforms(difficulty, other_platforms):
    while len(platforms) < 7:
        platforms_overlap = True

        tries = 0
        while platforms_overlap:
            prev_height = min([p.rect.top for p in other_platforms])

            new_platform = Platform(difficulty=difficulty, prev_height=prev_height)
            platforms_overlap = check_platform_overlap(new_platform, platforms)
            if platforms_overlap:
                tries += 1

            if tries >= 10:
                break  # Failsafe - allow platforms to overlap after 10 unsuccessful tries

        new_platform.generate_coin(coins)
        platforms.add(new_platform)
        all_sprites.add(new_platform)


def check_platform_overlap(new_platform, all_platforms):
    if pygame.sprite.spritecollideany(new_platform, all_platforms):
        return True
    else:
        for p in all_platforms:
            if p == new_platform:
                continue
            if (abs(new_platform.rect.top - p.rect.bottom) < 20) or (abs(new_platform.rect.bottom - p.rect.top) < 20):
                return True
        return False


# Initial platform
initial_platform = Platform(width=WIDTH)
initial_platform.rect = initial_platform.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
initial_platform.moving = False
initial_platform.point = False
initial_platform.base_platform = True

# Initialise player
player = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(initial_platform)
all_sprites.add(player)

platforms = pygame.sprite.Group()
platforms.add(initial_platform)

coins = pygame.sprite.Group()

pygame.mixer.init()
pygame.mixer.music.load('music/Stephen Helier - Study in A flat.wav')
pygame.mixer.music.play(-1)
pygame.event.wait()

while True:
    events = pygame.event.get()
    for event in events:
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
            if DEV_MODE and plat.base_platform:
                continue

            plat.rect.y += abs(player.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
        for coin in coins:
            coin.rect.y += abs(player.vel.y)
            if coin.rect.top >= HEIGHT:
                coin.kill()

    if len(platforms) < 7:
        difficulty = min(round(player.score/2), 100)  # Difficulty scales 0 - 100
        generate_platforms(difficulty=difficulty, other_platforms=platforms)

    player.update(platforms=platforms)
    player.move(events)

    for entity in all_sprites:
        display_surface.blit(entity.surf, entity.rect)

    for plat in platforms:
        plat.move(player)
        plat.check_crumble(player)

    for coin in coins:
        display_surface.blit(coin.image, coin.rect)
        coin.update(player)
        coin.move()

    check_score()

    pygame.display.update()
    FramePerSec.tick(FPS)
