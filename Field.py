import pygame

from main import all_sprites, tiles_group
from main import load_image


class Field(pygame.sprite.Sprite):
    image = load_image("mountains.png")

    def __init__(self, screen):
        super(Field, self).__init__(tiles_group, all_sprites)
