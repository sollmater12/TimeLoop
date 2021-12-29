import os
import sys

import pygame
import pygame_gui

from database_connect import Connection
from input_box import InputBox

FPS = 60
SIZE = WIDTH, HEIGHT = 600, 500
SCREEN = pygame.display.set_mode(SIZE)
BACKGROUND = pygame.Surface((800, 600))
BACKGROUND.fill(pygame.Color('#000000'))
CLOCK = pygame.time.Clock()
CONNECTION = Connection()


def load_image(filename, colorkey=None):
    fullname = os.path.join("data/img", filename)
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

    pygame.draw.rect(SCREEN, 'blue', (80, 350, 150, 20))

    pygame.draw.rect(SCREEN, 'red', (310, 350, 150, 20))


def start_screen():
    show_start_text()
    input1 = InputBox(305, 245)
    input2 = InputBox(305, 300)

    manager = pygame_gui.UIManager((800, 600))

    hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                                text='Say Hello',
                                                manager=manager)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = map(float, event.pos)
                if x in range(80, 231) and y in range(350, 370):
                    print(CONNECTION.check_user(input1.result, input2.result))
                elif x in range(310, 460) and y in range(350, 370):
                    CONNECTION.registration(input1.result, input2.result)
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == hello_button:
                        print('Hello World!')
            input1.handle_event(event)
            input2.handle_event(event)
            manager.process_events(event)
        # SCREEN.fill('#000000')

        show_start_text()

        input1.draw(SCREEN)
        input2.draw(SCREEN)

        SCREEN.blit(BACKGROUND, (0, 0))
        manager.draw_ui(SCREEN)

        pygame.display.update()

        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    start_screen()
