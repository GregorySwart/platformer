import pygame
import sys
from pygame.locals import *
import random
import time
from random import randint

pygame.init()
vec = pygame.math.Vector2  # 2 for two-dimensional

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
background_image = pygame.image.load("background.png")
background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("character.png")
        self.rect = self.surf.get_rect(center=(10, 420))

        self.pos = vec((10, 385))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.score = 0

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if P1.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point:
                        hits[0].point = False
                        self.score += 1
                    self.jumping = False
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -17

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3


class platform(pygame.sprite.Sprite):
    def __init__(self, width = 0, height = 18):
        super().__init__()

        if width == 0: width = random.randint(50, 120)

        self.image = pygame.image.load("platform.png")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = self.surf.get_rect(center = (random.randint(0, WIDTH-10),
                                                 random.randint(0, HEIGHT-30)))
        self.point = True
        self.speed = random.randint(-1, 1)
        self.moving = True

    def move(self):
        hits = self.rect.colliderect(P1.rect)
        if self.moving == True:
            self.rect.move_ip(self.speed, 0)
            if hits:
                P1.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

    def generateCoin(self):
        dice_roll = randint(1, 6)
        if (self.speed == 0) and dice_roll == 6:
            coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load("milk.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.topleft = pos

    def update(self):
        if self.rect.colliderect(P1.rect):
            P1.score += 10
            self.kill()


def check_score():
    point_platforms = [p for p in platforms if p.point]
    for p in point_platforms:
        if P1.rect.y < p.rect.y:
            P1.score += 0.1
            p.point = False


def plat_gen():
    while len(platforms) < 7 :
        width = random.randrange(50,100)
        C = True

        while C:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            C = check(p, platforms)

        p.generateCoin()
        platforms.add(p)
        all_sprites.add(p)


def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 10) or (abs(platform.rect.bottom - entity.rect.top) < 10):
                return True
        return False


# Initial platform
PT1 = platform(width=WIDTH)
PT1.rect = PT1.surf.get_rect(center=(WIDTH/2, HEIGHT - 10))
PT1.moving = False
PT1.point = False

# Initialise player
P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

coins = pygame.sprite.Group()

# Initial level generation
for x in range(random.randint(5, 6)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)

    pl.generateCoin()
    platforms.add(pl)
    all_sprites.add(pl)

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()

    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
        time.sleep(1)
        displaysurface.fill((255, 0, 0))
        pygame.display.update()
        time.sleep(1)
        pygame.quit()
        sys.exit()

    displaysurface.fill((0, 0, 0))

    displaysurface.blit(background, (0, 0))
    f = pygame.font.SysFont("Verdana", 20)
    g = f.render("Score:" + str(round(P1.score)), True, (123,255,0))
    text_rect = g.get_rect(center=(WIDTH/2, 20))
    displaysurface.blit(g, text_rect)

    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
        for coin in coins:
            coin.rect.y += abs(P1.vel.y)
            if coin.rect.top >= HEIGHT:
                coin.kill()

    if len(platforms) < 7:
        plat_gen()

    P1.update()

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    for coin in coins:
        displaysurface.blit(coin.image, coin.rect)
        coin.update()

    check_score()

    pygame.display.update()
    FramePerSec.tick(FPS)
