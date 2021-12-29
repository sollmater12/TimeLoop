import os
import sys

import pygame

from input_box import InputBox

FPS = 60
SIZE = WIDTH, HEIGHT = 600, 500
SCREEN = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()


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


def terminate():
    pygame.quit()
    sys.exit()


def show_start_text():
    intro_text = "Вход/Регистрация"
    font = pygame.font.Font(None, 50)
    string_rendered = font.render(intro_text, 1, pygame.Color('white'))
    SCREEN.blit(string_rendered, (150, 20))

    login = 'Введите имя пользователя:'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(login, 1, pygame.Color('white'))
    SCREEN.blit(string_rendered, (20, 250))

    password_field = 'Введите пароль:'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(password_field, 1, pygame.Color('white'))
    SCREEN.blit(string_rendered, (20, 301))


def start_screen():
    show_start_text()
    input1 = InputBox(305, 245)
    input2 = InputBox(305, 300)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            input1.handle_event(event)
            input2.handle_event(event)
        SCREEN.fill('black')
        show_start_text()
        input1.draw(SCREEN)
        input2.draw(SCREEN)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    start_screen()
