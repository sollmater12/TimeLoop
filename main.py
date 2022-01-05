import os
import sys
import time
import random

import pygame
import pygame_gui

from database_connect import Connection
from input_box import InputBox

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (750, 30)
FPS = 60
SIZE = WIDTH, HEIGHT = 507, 900
SIZE_2 = WIDTH_2, HEIGHT_2 = 507, 900
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption('TimeLoop')

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

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
        if self.rect.x < 400 and self.check_x == 1:
            self.rect.x += self.vx
        if self.rect.x == 400 and self.check_x == 1:
            self.check_x = -1
        if self.rect.x > 5 and self.check_x == -1:
            self.rect.x -= self.vx
        if self.rect.x == 5 and self.check_x == -1:
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


class Teleport(pygame.sprite.Sprite):
    image = load_image("tile1.png")

    def __init__(self, fls):
        super().__init__(tiles_group)
        self.image = Teleport.image
        self.rect = self.image.get_rect()
        self.fls = fls
        a = self.fls[-1]
        self.rect.x = random.randrange(20, 290)
        self.rect.y = random.randrange(a[1] - 100, a[1] - 80)
        self.fls += [(self.rect.x, self.rect.y)]
        direc = [-1, 1]
        self.check_x = random.choice(direc)
        self.vx = 1
        self.image = Teleport.image

    def update(self, *args, **kwargs) -> None:
        if self.rect.x < 400 and self.check_x == 1:
            self.rect.x += self.vx
        if self.rect.x == 400 and self.check_x == 1:
            self.check_x = -1
        if self.rect.x > 5 and self.check_x == -1:
            self.rect.x -= self.vx
        if self.rect.x == 5 and self.check_x == -1:
            self.check_x = 1

    def ret_fls(self):
        return self.fls


class Lava(pygame.sprite.Sprite):
    image = load_image("lava.png")
    image1 = load_image("lava1.png")
    flag = True

    def __init__(self):
        super().__init__(tiles_group)
        self.image = Lava.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 890
        self.check_x = 1
        self.vx = 1
        self.image = Lava.image

    def update(self, *args, **kwargs) -> None:
        self.rect.y -= self.vx


def show_start_text():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    SCREEN.blit(fon, (0, 0))
    intro_text = "Вход / Регистрация"
    font = pygame.font.Font(None, 50)
    string_rendered = font.render(intro_text, 1, pygame.Color(0, 0, 0))
    SCREEN.blit(string_rendered, (100, 100))

    login = 'Введите никнейм:'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(login, 1, pygame.Color(0, 0, 0))
    SCREEN.blit(string_rendered, (40, 255))

    password_field = 'Введите пароль:'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(password_field, 1, pygame.Color(0, 0, 0))
    SCREEN.blit(string_rendered, (40, 315))


def succesfull_text():
    text = 'Вы успешно вошли / зарегистрировались'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color(135, 144, 166))
    SCREEN.blit(string_rendered, (80, 600))


def failed_text():
    text = 'Имя уже занято / Имени не существует'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color(0, 0, 0))
    SCREEN.blit(string_rendered, (60, 600))


def draw_buttons(manager):
    login = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((130, 400), (100, 50)),
                                         text='Вход',
                                         manager=manager)
    registration = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 400), (100, 50)),
                                                text='Регистрация',
                                                manager=manager)

    return login, registration


def show_records():
    text = f'Мой рекорд: {CONNECTION.show_records()}'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color(0, 0, 0))
    SCREEN.blit(string_rendered, (180, 200))


def show_start_label():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    start_label = pygame.transform.scale(load_image('strt.png'), (100, 100))
    SCREEN.blit(fon, (0, 0))
    SCREEN.blit(start_label, (200, 300))
    start_label = pygame.transform.scale(load_image('rls.png'), (100, 100))
    SCREEN.blit(start_label, (200, 450))


def registration_screen():
    show_start_text()
    failed = True
    input1 = InputBox(270, 250)
    input2 = InputBox(270, 310)
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
    pygame.display.set_caption('TimeLoop')
    show_start_label()
    show_records()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and (200 <= event.pos[0] <= 300) and (300 <= event.pos[1] <= 400):
                fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
                start_label = pygame.transform.scale(load_image('strt.png'), (100, 100))
                start_label_1 = pygame.transform.scale(load_image('strt1.png'), (100, 100))
                start_label2 = pygame.transform.scale(load_image('rls.png'), (100, 100))
                SCREEN.blit(start_label_1, (200, 300))
                pygame.display.flip()
                time.sleep(0.25)
                SCREEN.blit(fon, (0, 0))
                show_records()
                SCREEN.blit(start_label, (200, 300))
                SCREEN.blit(start_label2, (200, 450))
                pygame.display.flip()
                time.sleep(0.5)
                return main_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and 200 <= event.pos[0] <= 300 and 450 <= event.pos[1] <= 550:
                fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
                start_label = pygame.transform.scale(load_image('strt.png'), (100, 100))
                start_label_1 = pygame.transform.scale(load_image('rls1.png'), (100, 100))
                start_label2 = pygame.transform.scale(load_image('rls.png'), (100, 100))
                SCREEN.blit(start_label_1, (200, 450))
                pygame.display.flip()
                time.sleep(0.25)
                SCREEN.blit(fon, (0, 0))
                show_records()
                SCREEN.blit(start_label, (200, 300))
                SCREEN.blit(start_label2, (200, 450))
                pygame.display.flip()
                time.sleep(0.5)
                return support_screen()
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
    text_coord = 20
    intro_text = ['TimeLoop - интересная аркадная игра, ',
                  'Которая увлечет не только малышей, ',
                  'Но и взрослых людей, ',
                  'Желающих с удовольствием скоротать время. ',
                  'Цель игры - преодалеть как можно ',
                  'Большее расстояние, ',
                  'Забраться на максимальную высоту. ',
                  'Представьте, что вы попали на планету, ',
                  'Где гравитация ничтожно мала, ',
                  'А также с помощью специального таймера ',
                  'Вы можете останавливать время. ',
                  'Да, вы не ослышались - останавливать время! ',
                  'Когда вы нажимаете кнопку на часах, ',
                  'Для вас время останавливается, ',
                  'Но оно начинает идти для окружающей ',
                  'Действительности. ',
                  'Повторное нажатие полностью меняет ситуацию',
                  'С точностью наоборот - вы двигаетесь, ',
                  'Для вас время идет, ',
                  'А все окружающее замерло. Но вот незадача - ',
                  'Вы умеете только прыгать вертикально вверх, ',
                  'Движения вбок недоступны. Чем выше вам ',
                  'Удастся забраться, тем круче. Удачи!']
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        SCREEN.blit(string_rendered, intro_rect)
        ret = pygame.transform.scale(load_image('return.png'), (100, 100))
        SCREEN.blit(ret, (200, 750))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and 200 <= event.pos[0] <= 300 and 750 <= event.pos[1] <= 850:
                start_screen()
        pygame.display.flip()
        CLOCK.tick(FPS)


def main_game():
    SCREEN = pygame.display.set_mode(SIZE_2)
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH_2, HEIGHT_2))
    hat = load_image('hat.png')
    hat0 = load_image('hat0.png')
    hat1 = load_image('hat1.png')
    SCREEN.blit(fon, (0, 0))
    SCREEN.blit(hat, (50, 50))
    fls = []
    for i in range(9):
        if i == 8:
            field = Teleport(fls)
            fls = field.ret_fls()
        else:
            field = Field(fls)
            fls = field.ret_fls()
    print(fls)
    player = Player()
    lava = Lava()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.change_direction(-1, 0)
                if event.key == pygame.K_RIGHT:
                    player.change_direction(1, 0)
                if event.key == pygame.K_UP:
                    player.change_direction(0, -1)
                if event.key == pygame.K_DOWN:
                    player.change_direction(0, 1)
                if event.key == pygame.K_SPACE:
                    player.change_direction(0, 0)
        SCREEN.blit(fon, (0, 0))
        SCREEN.blit(hat, (0, 0))
        player.update()
        tiles_group.update()
        player_group.draw(SCREEN)
        tiles_group.draw(SCREEN)
        CLOCK.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    registration_screen()
