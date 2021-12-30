import os
import sys

import pygame
import pygame_gui

from database_connect import Connection
from input_box import InputBox

FPS = 60
SIZE = WIDTH, HEIGHT = 600, 500
SCREEN = pygame.display.set_mode(SIZE)
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
    CONNECTION.connection.close()
    sys.exit()


def show_start_text():
    intro_text = "Вход/Регистрация"
    font = pygame.font.Font(None, 50)
    string_rendered = font.render(intro_text, 1, pygame.Color('white'))
    SCREEN.blit(string_rendered, (150, 20))

    login = 'Введите имя пользователя:'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(login, 1, pygame.Color('white'))
    SCREEN.blit(string_rendered, (20, 150))

    password_field = 'Введите пароль:'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(password_field, 1, pygame.Color('white'))
    SCREEN.blit(string_rendered, (20, 201))


def succesfull_text():
    text = 'Вы успешно вошли/зарегистрировались'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color('white'))
    SCREEN.blit(string_rendered, (80, 300))


def failed_text():
    text = 'Имя уже занято/Имени не существует'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color('white'))
    SCREEN.blit(string_rendered, (80, 300))


def draw_buttons(manager):
    login = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((80, 250), (100, 50)),
                                         text='Войти',
                                         manager=manager)
    registration = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((310, 250), (100, 50)),
                                                text='Регистрация',
                                                manager=manager)

    return login, registration


def start_screen():
    show_start_text()
    succesfull = False
    failed = False
    input1 = InputBox(305, 145)
    input2 = InputBox(305, 200)
    manager = pygame_gui.UIManager((600, 500))
    time_delta = CLOCK.tick(60) / 1000.0
    login, registration = draw_buttons(manager)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == login:
                        if CONNECTION.check_user(input1.check(), input2.check()):

                            failed = False
                            succesfull = True
                        else:
                            succesfull = False
                            failed = True
                    elif event.ui_element == registration:
                        if CONNECTION.registration(input1.check(), input2.check()):
                            failed = False
                            succesfull = True
                        else:
                            succesfull = False
                            failed = True
            manager.process_events(event)
            input1.handle_event(event)
            input2.handle_event(event)

        SCREEN.fill('#000000')
        manager.update(time_delta)

        show_start_text()
        if succesfull:
            succesfull_text()
        if failed:
            failed_text()

        manager.draw_ui(SCREEN)

        input1.draw(SCREEN)
        input2.draw(SCREEN)

        pygame.display.update()

        CLOCK.tick(60)


if __name__ == '__main__':
    pygame.init()
    start_screen()
