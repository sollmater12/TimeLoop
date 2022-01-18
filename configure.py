import os
import pygame
import sys


FPS = 60
SIZE = WIDTH, HEIGHT = 507, 900
SCREEN = pygame.display.set_mode(SIZE)
SIZE_2 = WIDTH_2, HEIGHT_2 = 507, 900
START_HEIGHT = 900
ACC = 0.5
FRIC = -0.12
vec = pygame.math.Vector2



# Функция загрузки изображений
def load_image(filename, colorkey=None):
    fullname = os.path.join(filename)
    if not os.path.isfile(fullname):
        # print('File is not found!')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
