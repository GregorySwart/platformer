import pygame


class Coin(pygame.sprite.Sprite):
    """ Collectibles for the player to collect, increases score by 10 upon collection. Currently, these look like
    glasses of milk. Will disappear after 3 seconds if nto collected. """
    def __init__(self, pos, speed):
        super().__init__()

        self.image = pygame.image.load("data/milk_full.png").convert_alpha()
        self.surf = pygame.transform.scale(self.image, (45, 45))
        self.rect = self.image.get_rect()

        self.rect.center = pos
        self.time_generated = None
        self.points = 15
        self.speed = speed
        self.platform = None

    def update(self, player):
        now = pygame.time.get_ticks()

        if self.rect.colliderect(player.rect):
            player.score += self.points
            self.kill()

        if not self.time_generated:
            if self.rect.centery > 0:
                self.time_generated = now
        else:
            if now - self.time_generated > 3000:
                self.image = pygame.image.load("data/milk_empty.png")
                self.points = 1
            elif now - self.time_generated > 2000:
                self.image = pygame.image.load("data/milk_2.png")
                self.points = 5
            elif now - self.time_generated > 1000:
                self.image = pygame.image.load("data/milk_1.png")
                self.points = 10

    def move(self):
        if self.speed:
            self.rect.move_ip(self.speed, 0)
