import os
import sys
import time

import pygame
import pygame_gui

from database_connect import Connection
from input_box import InputBox

FPS = 60
SIZE = WIDTH, HEIGHT = 600, 500
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Авторизация')

SIZE_2 = WIDTH_2, HEIGHT_2 = 600, 500
SCREEN_2 = pygame.display.set_mode(SIZE_2)

SIZE_3 = WIDTH_3, HEIGHT_3 = 600, 500
SCREEN_3 = pygame.display.set_mode(SIZE_3)

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
    string_rendered = font.render(intro_text, 1, pygame.Color(135, 144, 166))
    SCREEN.blit(string_rendered, (150, 20))

    login = 'Введите имя пользователя:'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(login, 1, pygame.Color(135, 144, 166))
    SCREEN.blit(string_rendered, (20, 150))

    password_field = 'Введите пароль:'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(password_field, 1, pygame.Color(135, 144, 166))
    SCREEN.blit(string_rendered, (20, 201))


def succesfull_text():
    text = 'Вы успешно вошли/зарегистрировались'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color(135, 144, 166))
    SCREEN.blit(string_rendered, (80, 300))


def failed_text():
    text = 'Имя уже занято/Имени не существует'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color(135, 144, 166))
    SCREEN.blit(string_rendered, (80, 300))


def draw_buttons(manager):
    login = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 250), (100, 50)),
                                         text='Войти',
                                         manager=manager)
    registration = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 250), (100, 50)),
                                                text='Регистрация',
                                                manager=manager)

    return login, registration


def show_records():
    text = f'Ваш рекорд: {CONNECTION.show_records()}'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color(135, 144, 166))
    SCREEN_2.blit(string_rendered, (140, 100))


def show_start_label():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    start_label = load_image('strt.png')
    SCREEN_2.blit(fon, (0, 0))
    SCREEN_2.blit(start_label, (-15, 100))
    start_label = load_image('rls.png')
    SCREEN_2.blit(start_label, (-15, 200))


def registration_screen():
    show_start_text()
    failed = True
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
                            return start_screen()
                        else:
                            failed = False
                    elif event.ui_element == registration:
                        if CONNECTION.registration(input1.check(), input2.check()):
                            return start_screen()
                        else:
                            failed = False
            manager.process_events(event)
            input1.handle_event(event)
            input2.handle_event(event)

        SCREEN.fill((255, 255, 255))
        manager.update(time_delta)

        show_start_text()
        if failed is not True:
            failed_text()
        manager.draw_ui(SCREEN)

        input1.draw(SCREEN)
        input2.draw(SCREEN)

        pygame.display.update()

        CLOCK.tick(60)


def start_screen():
    pygame.display.set_caption('Начальный экран')
    show_start_label()
    show_records()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and 140 <= event.pos[0] <= 560 and 200 <= event.pos[1] <= 300:
                start_label = load_image('strt.png')
                start_label_1 = load_image('strt1.png')
                SCREEN_2.blit(start_label_1, (-15, 100))
                pygame.display.flip()
                time.sleep(0.25)
                SCREEN_2.blit(start_label, (-15, 100))
                start_label = load_image('rls.png')
                SCREEN_2.blit(start_label, (-15, 200))
                pygame.display.flip()
                time.sleep(1)
                print(0)  # начинаем игру
            elif event.type == pygame.MOUSEBUTTONDOWN and 140 <= event.pos[0] <= 560 and 300 <= event.pos[1] <= 400:
                return support_screen()  # начинаем игру
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(13):
                    b = i + 5
                    a = load_image(str(b) + '.png')
                    SCREEN_2.blit(a, (event.pos[0] - 450, event.pos[1] - 300))
                    pygame.display.flip()
                    time.sleep(0.0001)
                    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
                    start_label_1 = load_image('strt.png')
                    rules_label = load_image('rls.png')
                    SCREEN_2.blit(fon, (0, 0))
                    SCREEN_2.blit(start_label_1, (-15, 100))
                    SCREEN_2.blit(rules_label, (-15, 200))
                    show_records()
                    pygame.display.flip()
        pygame.display.flip()


def support_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    SCREEN_3.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 0
    intro_text = ['TimeLoop - интересная аркадная игра, ',
           'которая увлечет не только малышей, но и взрослых людей, ',
           'желающих с удовольствием скоротать время. ',
           'Цель игры - преодалеть как можно большее расстояние, ',
           'забраться на максимальную высоту. ',
           'Представьте, что вы попали на планету, где гравитация ничтожно мала, ',
           'а также с помощью специального таймера вы можете останавливать время. ',
           'Да-да, вы не ослышались - останавливать время! ',
           'Когда вы нажимаете кнопку на часах, для вас время останавливается, ',
           'но оно начинает идти для окружающей действительности. ',
           'Повторное нажатие кардинально меняет ситуацию с точностью наоборот - вы двигаетесь, для вас время идет, ',
           'а все окружающее замерло. Но вот незадача - вы умеете только прыгать вертикально вверх, ',
           'движения вбок недоступны. Чем выше вам удастся забраться, тем круче. Удачи!']
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        SCREEN_3.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_screen()
        pygame.display.flip()
        CLOCK.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    registration_screen()
