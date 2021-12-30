import time

import pygame
import sys
import os

pygame.init()
SIZE = WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode(SIZE)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(filename, colorkey=None):
    fullname = os.path.join("data", filename)
    if not os.path.isfile(fullname):
        print('File is not found!')
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


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    strt = load_image('strt.png')
    screen.blit(fon, (0, 0))
    screen.blit(strt, (15, 100))
    strtr = strt.get_rect()
    print(strtr)
    # font = pygame.font.Font(None, 30)
    # text_coord = 50
    # for line in intro_text:
    #     string_rendered = font.render(line, 1, pygame.Color('black'))
    #     intro_rect = string_rendered.get_rect()
    #     text_coord += 10
    #     intro_rect.top = text_coord
    #     intro_rect.x = 10
    #     text_coord += intro_rect.height
    #     screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and 140 <= event.pos[0] <= 560 and 200 <= event.pos[1] <= 300:
                strt1 = load_image('strt1.png')
                screen.blit(strt1, (15, 100))
                pygame.display.flip()
                time.sleep(0.25)
                screen.blit(strt, (15, 100))
                pygame.display.flip()
                time.sleep(1)
                return print(0)  # начинаем игру
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(13):
                    b = i + 5
                    a = load_image(str(b) + '.png')
                    screen.blit(a, (event.pos[0] - 450, event.pos[1] - 300))
                    pygame.display.flip()
                    time.sleep(0.0001)
                    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
                    strt = load_image('strt.png')
                    screen.blit(fon, (0, 0))
                    screen.blit(strt, (15, 100))
                    pygame.display.flip()
        pygame.display.flip()


if __name__ == '__main__':
    start_screen()
