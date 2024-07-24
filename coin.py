import pygame


class Coin(pygame.sprite.Sprite):
    """ Collectibles for the player to collect, increases score by 10 upon collection. Currently, these look like
    glasses of milk. Will disappear after 3 seconds if nto collected. """
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load("data/milk.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.topleft = pos
        self.time_generated = None

    def update(self, player):
        now = pygame.time.get_ticks()

        if self.rect.colliderect(player.rect):
            player.score += 10
            self.kill()

        if not self.time_generated:
            if self.rect.top > 0:
                self.time_generated = now
        else:
            if now - self.time_generated > 3000:
                self.kill()
