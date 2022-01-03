import os
import sys
import time
import random

import pygame
import pygame_gui

from database_connect import Connection
from input_box import InputBox

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (750, 30) # меняем расположение окна
FPS = 60
SIZE = WIDTH, HEIGHT = 600, 500
SIZE_2 = WIDTH_2, HEIGHT_2 = 507, 900
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Авторизация')

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

CLOCK = pygame.time.Clock()
CONNECTION = Connection()
PLAYER_TURN = True


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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__(player_group, all_sprites)
        self.image = load_image('player.png')
        self.pos_x = 300
        self.pos_y = 800
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)
        self.vx = 0
        self.vy = 0

    def change_direction(self, x, y):
        self.vx = x
        self.vy = y

    def update(self, *args, **kwargs) -> None:
        if self.pos_x + self.vx in range(0, 484) and self.pos_y + self.vy in range(0, 861):
            self.pos_x += self.vx
            self.pos_y += self.vy
            self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)


class Field(pygame.sprite.Sprite):
    image = load_image("check_draw.png")

    def __init__(self, fls):
        super().__init__(tiles_group)
        self.image = Field.image
        self.rect = self.image.get_rect()
        self.fls = fls
        if len(self.fls) == 0:
            self.rect.x = random.randrange(20, 290)
            self.rect.y = random.randrange(860, 880)
            self.fls += [(self.rect.x, self.rect.y)]
            self.check_x = -1
        elif len(self.fls) == 1:
            t = random.randrange(1, 3)
            print(t)
            if t == 1:
                a = self.fls[-1]
                self.rect.x = random.randrange(20, 50)
                self.rect.y = random.randrange(a[1] - 100, a[1] - 80)
                self.fls += [(self.rect.x, self.rect.y)]
                self.check_x = 1
            elif t == 2:
                a = self.fls[-1]
                self.rect.x = random.randrange(250, 290)
                self.rect.y = random.randrange(a[1] - 100, a[1] - 80)
                self.fls += [(self.rect.x, self.rect.y)]
                self.check_x = -1
        # while len(pygame.sprite.spritecollide(self, tiles_group, False)) != 1:
        #     self.rect.x = random.randrange(200, 307)
        #     self.rect.y = random.randrange(28, 900)
        else:
            a = self.fls[-1]
            if 0 <= a[0] <= 150:
                b = random.randrange(250, 290)
                self.check_x = -1
            else:
                b = random.randrange(41, 150)
                self.check_x = 1
            self.rect.x = random.randrange(b - 40, b)
            self.rect.y = random.randrange(a[1] - 100, a[1] - 80)
            self.fls += [(self.rect.x, self.rect.y)]
        self.vx = 1
        self.image = Field.image

    def update(self, *args, **kwargs) -> None:
        if self.rect.x < 290 and self.check_x == 1:
            self.rect.x += self.vx
        if self.rect.x == 290 and self.check_x == 1:
            self.check_x = -1
        if self.rect.x > 20 and self.check_x == -1:
            self.rect.x -= self.vx
        if self.rect.x == 20 and self.check_x == -1:
            self.check_x = 1
        # if self.check_y - 20 <= self.rect.y <= self.check_y + 20:
        #     self.rect.y += self.vx
        # if self.rect.y + 1 > self.check_y + 20:
        #     self.vx = -1
        #     self.rect.y += self.vx
        # if self.rect.y <= self.check_y - 20:
        #     self.vx = 1
        #     self.rect.y += self.vx

    def ret_fls(self):
        return self.fls


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
    SCREEN.blit(string_rendered, (140, 100))


def show_start_label():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    start_label = load_image('strt.png')
    SCREEN.blit(fon, (0, 0))
    SCREEN.blit(start_label, (-15, 100))
    start_label = load_image('rls.png')
    SCREEN.blit(start_label, (-15, 200))


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
    SCREEN = pygame.display.set_mode(SIZE)
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
                SCREEN.blit(start_label_1, (-15, 100))
                pygame.display.flip()
                time.sleep(0.25)
                SCREEN.blit(start_label, (-15, 100))
                start_label = load_image('rls.png')
                SCREEN.blit(start_label, (-15, 200))
                pygame.display.flip()
                time.sleep(1)
                return main_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and 140 <= event.pos[0] <= 560 and 300 <= event.pos[1] <= 400:
                return support_screen()  # начинаем игру
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(13):
                    b = i + 5
                    a = load_image(str(b) + '.png')
                    SCREEN.blit(a, (event.pos[0] - 450, event.pos[1] - 300))
                    pygame.display.flip()
                    time.sleep(0.0001)
                    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
                    start_label_1 = load_image('strt.png')
                    rules_label = load_image('rls.png')
                    SCREEN.blit(fon, (0, 0))
                    SCREEN.blit(start_label_1, (-15, 100))
                    SCREEN.blit(rules_label, (-15, 200))
                    show_records()
                    pygame.display.flip()
        pygame.display.flip()


def support_screen():
    SCREEN = pygame.display.set_mode(SIZE)
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    SCREEN.blit(fon, (0, 0))
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
        SCREEN.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_screen()
        pygame.display.flip()
        CLOCK.tick(FPS)


def player_movement_label():
    text = 'Ваш ход'
    font = pygame.font.Font(None, 45)
    string_rendered = font.render(text, 1, pygame.Color(0, 0, 0))
    SCREEN.blit(string_rendered, (0, 0))


def tile_movement_label():
    text = 'Ход игры'
    font = pygame.font.Font(None, 45)
    string_rendered = font.render(text, 1, pygame.Color(0, 0, 0))
    SCREEN.blit(string_rendered, (0, 0))


def main_game():
    global PLAYER_TURN
    SCREEN = pygame.display.set_mode(SIZE_2)
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH_2, HEIGHT_2))
    SCREEN.blit(fon, (0, 0))
    fls = []
    for i in range(10):
        field = Field(fls)
        fls = field.ret_fls()
    print(fls)
    player = Player()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:  # добавляем передвижение по кнопкам и отправляем направление в функциюя класса
                if event.key == pygame.K_UP:
                    player.change_direction(0, -1)
                if event.key == pygame.K_DOWN:
                    player.change_direction(0, 1)
                if event.key == pygame.K_SPACE:  # при нажатии на пробел меняем ход персонажа на движение плит и наоборот
                    player.change_direction(0, 0)
                    PLAYER_TURN = not PLAYER_TURN
        SCREEN.blit(fon, (0, 0))
        if PLAYER_TURN:  # если ход персонажа, то выводит этот текст на экран и обновляем только движения персонажа
            player_movement_label()
            player.update()
        else:
            tile_movement_label()
            tiles_group.update()
        tiles_group.draw(SCREEN)
        player_group.draw(SCREEN)
        CLOCK.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    registration_screen()
