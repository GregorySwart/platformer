import pygame


class Coin(pygame.sprite.Sprite):
    """ Collectibles for the player to collect, increases score by 10 upon collection. Currently, these look like
    glasses of milk. """
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load("data/milk.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.topleft = pos

    def update(self, player):
        if self.rect.colliderect(player.rect):
            player.score += 10
            self.kill()
