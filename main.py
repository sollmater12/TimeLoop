import os  # ЗДРАВСТВУЙТЕ, КСЕНИЯ АНДРЕЕВНА!
import sys
import time
import random

import pygame
import pygame_gui

from database_connect import Connection
from input_box import InputBox

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (750, 30)  # Задаем константы
FPS = 60
SIZE = WIDTH, HEIGHT = 507, 900
SIZE_2 = WIDTH_2, HEIGHT_2 = 507, 900
START_HEIGHT = 0
SCREEN = pygame.display.set_mode(SIZE)
ACC = 0.5
FRIC = -0.12
pygame.display.set_caption('TimeLoop')

all_sprites = pygame.sprite.Group()  # Создаем группы спрайтов
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tele_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
kill_group = pygame.sprite.Group()
good_blocks = pygame.sprite.Group()
fon = pygame.sprite.Group()
coin = pygame.sprite.Group()

CLOCK = pygame.time.Clock()
CONNECTION = Connection()
PLAYER_TURN = False

FIRST_X, FIRST_Y = 0, 0

vec = pygame.math.Vector2


# Функция загрузки изображений
def load_image(filename, colorkey=None):
    fullname = os.path.join("data/img", filename)
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


# Функция "убийства" программы
def terminate():
    pygame.quit()
    CONNECTION.connection.close()
    sys.exit()


# Класс персонажа
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        global START_HEIGHT
        super(Player, self).__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(load_image('player.png'), (25, 43))
        # print(x)
        # print(y)
        self.rect = self.image.get_rect()
        self.pos = vec(FIRST_X + 15, FIRST_Y - 35)
        START_HEIGHT = FIRST_Y - 35
        self.vel = vec(0, 0)
        self.acc = vec(0, 0.5)
        # print(self.pos[0])
        # print(self.pos[1])
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        self.isJump = False

    def change_direction(self, x, y):
        self.vx = x
        self.vy = y

    def move(self, check):
        self.acc = vec(0, 0.1)
        # pressed_keys = pygame.key.get_pressed()
        #
        # if pressed_keys[K_LEFT]:
        #     self.acc.x = -ACC
        # if pressed_keys[K_RIGHT]:
        #     self.acc.x = ACC
        #
        # self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # if self.pos.x > WIDTH:
        #     self.pos.x = 0
        # if self.pos.x < 0:
        #     self.pos.x = WIDTH
        # if not check or self.isJump is True:
        self.rect.midbottom = self.pos
        self.isJump = False
        if self.vel.y > 0 and check:
            self.pos.y = check[0].rect.top + 1
            self.vel.y = 0

    def update(self, check):
        if check:
            if check[-1].rect.x <= 400 and check[-1].check_x == 1:
                self.pos.x += check[0].vx / FPS
            if check[-1].rect.x > 400 and check[-1].check_x == 1:
                self.check_x = -1
            if check[-1].rect.x >= 5 and check[-1].check_x == -1:
                self.pos.x -= check[0].vx / FPS
            if check[-1].rect.x < 5 and check[-1].check_x == -1:
                self.check_x = 1

    def get_coord(self):
        return [self.rect.x, self.rect.y]

    def jump(self):
        hits = pygame.sprite.spritecollide(self, tiles_group, False)
        if hits:
            self.vel.y = -4


# Класс тайлов, по которым прыгает перс
class Field(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('check_draw.png'), (50, 13))

    def __init__(self, fls):
        global FIRST_X, FIRST_Y
        super().__init__(tiles_group, good_blocks, all_sprites)
        self.image = Field.image
        self.rect = self.image.get_rect()
        self.fls = fls
        if len(self.fls) == 0:
            self.rect.x = random.randrange(20, 290)
            self.rect.y = random.randrange(880, 890)
            self.fls += [(self.rect.x, self.rect.y)]
            self.check_x = -1
            FIRST_X = self.rect.x
            FIRST_Y = self.rect.y
        elif len(self.fls) == 1:
            t = random.randrange(1, 3)
            # print(t)
            if t == 1:
                a = self.fls[-1]
                self.rect.x = random.randrange(20, 50)
                self.rect.y = random.randrange(a[1] - 100, a[1] - 90)
                self.fls += [(self.rect.x, self.rect.y)]
                self.check_x = 1
            elif t == 2:
                a = self.fls[-1]
                self.rect.x = random.randrange(250, 290)
                self.rect.y = random.randrange(a[1] - 100, a[1] - 90)
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
            self.rect.y = random.randrange(a[1] - 80, a[1] - 60)
            self.fls += [(self.rect.x, self.rect.y)]
        self.vx = random.choice([60, 120, 180])  # Этот параметр отвечает за скорость. Если его менять, то плиты останавливаются в конце экрана
        self.image = Field.image

    def update(self, *args, **kwargs) -> None:
        if self.rect.x <= 400 and self.check_x == 1:
            self.rect.x += self.vx / FPS  # Если же здесь добавить ФПС, то все будет дико лагать. То же самое в классах Телепорт и Киллер. В Лаве же ФПС работает
        if self.rect.x > 400 and self.check_x == 1:
            self.check_x = -1
        if self.rect.x >= 5 and self.check_x == -1:
            self.rect.x -= self.vx / FPS
        if self.rect.x < 5 and self.check_x == -1:
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


# Класс плиты, которая перемещает на следующий уровень
class Teleport(pygame.sprite.Sprite):
    image = load_image("tile1.png")

    def __init__(self, fls):
        super().__init__(tele_group, good_blocks, all_sprites)
        self.image = Teleport.image
        self.rect = self.image.get_rect()
        self.fls = fls
        a = self.fls[-1]
        self.rect.x = random.randrange(20, 290)
        self.rect.y = random.randrange(a[1] - 80, a[1] - 60)
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


# Класс плиты-убийцы. Ее касаться нельзя
class Killer(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('tile_kill2.png'), (150, 26))

    def __init__(self):
        super().__init__(kill_group, all_sprites)
        self.image = Killer.image
        self.rect = self.image.get_rect()
        self.rect.x = -249
        self.rect.y = random.randrange(60, 700)
        while pygame.sprite.spritecollide(self, good_blocks, False) or pygame.sprite.spritecollide(self, player_group,
                                                                                                   False):
            self.rect.y = random.randrange(60, 880)
        direc = [-1, 1]
        self.check_x = random.choice(direc)
        self.vx = random.choice([60, 120, 180])
        self.image = Killer.image

    def update(self, *args, **kwargs) -> None:
        self.rect.x += self.vx / FPS
        if self.rect.x > 507:
            self.rect.x = -249
        # if self.rect.x < 350 and self.check_x == 1:
        #     self.rect.x += self.vx
        # if self.rect.x == 350 and self.check_x == 1:
        #     self.check_x = -1
        # if self.rect.x > 5 and self.check_x == -1:
        #     self.rect.x -= self.vx
        # if self.rect.x == 5 and self.check_x == -1:
        #     self.check_x = 1


# Класс условной лавы. Она поднимается с определенной скоростью снизу, заставляя игрока  думать быстрее
class Lava(pygame.sprite.Sprite):
    image = load_image("lava1.png")
    image1 = load_image("lava2.png")
    flag = True
    count = 0

    def __init__(self):
        super().__init__(lava_group, all_sprites)
        self.image = Lava.image1
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 2400
        self.check_x = 1
        self.vx = 60
        self.image = Lava.image1

    def update(self, *args, **kwargs) -> None:
        self.rect.y -= self.vx / FPS


# Класс монетки, которую надо собирать, но еще счетчки их, как и счетчик расстояния и в конечном счете рекорда, не доделан
class Coin(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('cn.png'), (50, 50))

    def __init__(self):
        super().__init__(coin, all_sprites)
        self.image = Coin.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(5, 450)
        self.rect.y = random.randrange(100, 850)
        self.image = Coin.image


# Функция отрисовки текста на регистрационном окне
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


# Сейчас не используется, когда будем наводить лоск в проекте - уберем
def succesfull_text():
    text = 'Вы успешно вошли / зарегистрировались'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color(135, 144, 166))
    SCREEN.blit(string_rendered, (80, 600))


# Отрисовка текста, если произошла какая-то ошибка с именем или паролем
def failed_text():
    text = 'Имя уже занято / Имени не существует'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color(0, 0, 0))
    SCREEN.blit(string_rendered, (60, 600))


# Рисуем кнопочки на рег окне
def draw_buttons(manager):
    login = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((130, 400), (100, 50)),
                                         text='Вход',
                                         manager=manager)
    registration = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 400), (100, 50)),
                                                text='Регистрация',
                                                manager=manager)

    return login, registration


# Функция показа рекорда из БД в главном меню. Пока рекорд не обновляется, доделаем
def show_records():
    text = f'Мой рекорд: {CONNECTION.show_records()}'
    text_2 = f'Количество монет: {CONNECTION.show_money()}'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color(0, 0, 0))
    string_rendered_2 = font.render(text_2, 1, pygame.Color(0, 0, 0))
    SCREEN.blit(string_rendered, (180, 200))
    SCREEN.blit(string_rendered_2, (160, 225))



# def res(step):
#     text = f'{step} m'
#     font = pygame.font.Font(None, 30)
#     string_rendered = font.render(text, 1, pygame.Color(0, 0, 0))
#     SCREEN.blit(string_rendered, (10, 100))

# Рисуем кнопочки в главном меню
def show_start_label():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    start_label = pygame.transform.scale(load_image('strt.png'), (100, 100))
    SCREEN.blit(fon, (0, 0))
    SCREEN.blit(start_label, (200, 300))
    start_label = pygame.transform.scale(load_image('rls.png'), (100, 100))
    SCREEN.blit(start_label, (200, 450))

def show_current_records(record):
    text = f'Счет: {record}'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color(0, 0, 0))
    SCREEN.blit(string_rendered, (0, 60))


# Отрабатываем ввод текста в рег окне
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
                    try:
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
                    except Exception:
                        failed_text()
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


# Механика работы кнопок в главном меню плюс микро-пасхалочка
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
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     for i in range(13):
            #         b = i + 5
            #         a = load_image(str(b) + '.png')
            #         SCREEN.blit(a, (event.pos[0] - 450, event.pos[1] - 300))
            #         pygame.display.flip()
            #         time.sleep(0.0001)
            #         fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
            #         start_label_1 = pygame.transform.scale(load_image('strt.png'), (100, 100))
            #         rules_label = pygame.transform.scale(load_image('rls.png'), (100, 100))
            #         SCREEN.blit(fon, (0, 0))
            #         SCREEN.blit(start_label_1, (200, 300))
            #         SCREEN.blit(rules_label, (200, 450))
            #         show_records()
            #         pygame.display.flip()
        pygame.display.flip()


# Рисуем экран с правилами
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
                  'Удастся забраться, тем круче. Удачи!',
                  "Для прыжка жмите на пробел,",
                  "Для смены времени - на Д (L).",
                  "Собирайте монеты и бейте рекорды!"]
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        SCREEN.blit(string_rendered, intro_rect)
        ret = pygame.transform.scale(load_image('return.png'), (100, 100))
        SCREEN.blit(ret, (200, 800))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and 200 <= event.pos[0] <= 300 and 800 <= event.pos[1] <= 900:
                start_screen()
        pygame.display.flip()
        CLOCK.tick(FPS)


# Меню паузы
def stop_menu(help_count_len):
    global all_sprites, tiles_group, lava_group, player_group,tele_group, kill_group, PLAYER_TURN, count, count1, count2
    CONNECTION.add_money(count2)
    CONNECTION.check_record(help_count_len)
    a = True
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH_2, HEIGHT_2))
    while a:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and 120 <= event.pos[0] <= 180 and 400 <= event.pos[1] <= 465:
                all_sprites.empty()
                tiles_group.empty()
                player_group.empty()
                tele_group.empty()
                lava_group.empty()
                kill_group.empty()
                good_blocks.empty()
                all_sprites = pygame.sprite.Group()  # Создаем группы спрайтов
                tiles_group = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                tele_group = pygame.sprite.Group()
                lava_group = pygame.sprite.Group()
                kill_group = pygame.sprite.Group()

                a = False
            if event.type == pygame.MOUSEBUTTONDOWN and 205 <= event.pos[0] <= 275 and 400 <= event.pos[1] <= 465:
                a = False
                all_sprites.empty()
                tiles_group.empty()
                player_group.empty()
                tele_group.empty()
                lava_group.empty()
                kill_group.empty()
                good_blocks.empty()
                all_sprites = pygame.sprite.Group()  # Создаем группы спрайтов
                tiles_group = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                tele_group = pygame.sprite.Group()
                lava_group = pygame.sprite.Group()
                kill_group = pygame.sprite.Group()
                PLAYER_TURN = False
                count2 = 0
                count1 = 0
                count = 0
                main_game()
            if event.type == pygame.MOUSEBUTTONDOWN and 290 <= event.pos[0] <= 370 and 400 <= event.pos[1] <= 465:
                a = False
                all_sprites.empty()
                tiles_group.empty()
                player_group.empty()
                tele_group.empty()
                lava_group.empty()
                kill_group.empty()
                good_blocks.empty()
                all_sprites = pygame.sprite.Group()  # Создаем группы спрайтов
                tiles_group = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                tele_group = pygame.sprite.Group()
                lava_group = pygame.sprite.Group()
                kill_group = pygame.sprite.Group()
                PLAYER_TURN = False
                count2 = 0
                count1 = 0
                count = 0
                start_screen()


# def end_game_screen():
#     global all_sprites, tiles_group, lava_group, player_group
#     SCREEN = pygame.display.set_mode(SIZE_2)
#     fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH_2, HEIGHT_2))
#     SCREEN.blit(fon, (0, 0))
#     text = f'Вы проиграли'
#     font = pygame.font.Font(None, 45)
#     string_rendered = font.render(text, 1, pygame.Color(0, 0, 0))
#     SCREEN.blit(string_rendered, (145, 300))
#     manager = pygame_gui.UIManager((507, 900))
#     time_delta = CLOCK.tick(60) / 1000.0
#     restart, menu = draw_buttons_2(manager)
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 terminate()
#             if event.type == pygame.USEREVENT:
#                 if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
#                     if event.ui_element == restart:
#                         all_sprites = pygame.sprite.Group()
#                         tiles_group = pygame.sprite.Group()
#                         lava_group = pygame.sprite.Group()
#                         player_group = pygame.sprite.Group()
#                         return main_game()
#                     elif event.ui_element == menu:
#                         all_sprites = pygame.sprite.Group()
#                         tiles_group = pygame.sprite.Group()
#                         lava_group = pygame.sprite.Group()
#                         player_group = pygame.sprite.Group()
#                         return start_screen()
#             manager.process_events(event)
#         manager.update(time_delta)
#         manager.draw_ui(SCREEN)
#         CLOCK.tick(FPS)
#         pygame.display.flip()

# Экран смерти - то есть при проигрыше
def end(help_count_len):
    global all_sprites, tiles_group, player_group, kill_group, tele_group, lava_group, PLAYER_TURN, count, count1, count2
    PLAYER_TURN = False
    count2 = 0
    count1 = 0
    count = 0
    die = load_image('die.png')
    SCREEN.blit(die, (0, 0))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and 115 <= event.pos[0] <= 195 and 380 <= event.pos[1] <= 450:
                running = False
                all_sprites.empty()
                tiles_group.empty()
                player_group.empty()
                tele_group.empty()
                lava_group.empty()
                kill_group.empty()
                good_blocks.empty()
                all_sprites = pygame.sprite.Group()  # Создаем группы спрайтов
                tiles_group = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                tele_group = pygame.sprite.Group()
                lava_group = pygame.sprite.Group()
                kill_group = pygame.sprite.Group()
                CONNECTION.add_money(count2)
                CONNECTION.check_record(help_count_len)
                return main_game()
            if event.type == pygame.MOUSEBUTTONDOWN and 255 <= event.pos[0] <= 340 and 370 <= event.pos[1] <= 450:
                running = False
                all_sprites.empty()
                tiles_group.empty()
                player_group.empty()
                tele_group.empty()
                lava_group.empty()
                kill_group.empty()
                good_blocks.empty()
                all_sprites = pygame.sprite.Group()  # Создаем группы спрайтов
                tiles_group = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                tele_group = pygame.sprite.Group()
                lava_group = pygame.sprite.Group()
                kill_group = pygame.sprite.Group()
                CONNECTION.add_money(count2)
                CONNECTION.check_record(help_count_len)
                return start_screen()


def show_coins(count):
    text = f'Монеты: {count}'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color(0, 0, 0))
    SCREEN.blit(string_rendered, (0, 80))


count1 = 0  # Счетчик расстояния будет
count2 = 0


# Функция работы основной игры
def main_game():
    global PLAYER_TURN, all_sprites, tiles_group, player_group, count1, coin, kill_group, tele_group, count1, count2
    SCREEN = pygame.display.set_mode(SIZE_2)
    help_count_len = count1
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    hat = load_image('hat.png')
    fon1 = load_image('fon1.png')
    hat0 = load_image('hat0.png')
    hat1 = load_image('hat1.png')
    clc = pygame.transform.scale(load_image('clc.png'), (74, 109))
    clc1 = pygame.transform.scale(load_image('clc1.png'), (74, 109))
    hat0 = load_image('hat0.png')
    SCREEN.blit(hat, (50, 50))
    SCREEN.blit(clc, (430, 790))  # Вплоть до сюда рисуем элементы интерфейса
    b = False
    fls = []  # Список с координатами плит
    for i in range(12):  # Генерация плит
        if i == 11:
            field = Teleport(fls)
            tele_group.add(field)
            good_blocks.add(field)
            fls = field.ret_fls()
        else:
            field = Field(fls)
            tiles_group.add(field)
            good_blocks.add(field)
            fls = field.ret_fls()
    # print(fls)  # Дебаг :)
    num = random.randint(1, 3)
    if num == 1:
        kill = Killer()
    elif num == 2:
        kill = Killer()
        kill = Killer()
    else:
        kill = Killer()
        kill = Killer()
        kill = Killer()
    print(kill_group)
    lava = Lava()
    player = Player(fls[0][0], fls[0][1])
    # coord = player.get_coord()[1]
    cn = Coin()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Прыжок перса
                    if PLAYER_TURN:
                        player.isJump = True
                        player.jump()
                    # count1 += abs(player.get_coord()[1] - 900 + coord)
            if event.type == pygame.MOUSEBUTTONDOWN and 410 <= event.pos[0] <= 470 and 0 <= event.pos[
                1] <= 50:  # Ставимся на паузу
                SCREEN.blit(hat0, (0, 0))
                SCREEN.blit(hat1, (0, 0))
                pygame.display.flip()
                time.sleep(0.25)
                SCREEN.blit(hat0, (0, 0))
                SCREEN.blit(hat, (0, 0))
                stp = load_image('stp.png')
                SCREEN.blit(stp, (0, 0))
                pygame.display.flip()
                stop_menu(help_count_len)
            if (event.type == pygame.MOUSEBUTTONDOWN and 359 <= event.pos[0] <= 507 and 683 <= event.pos[1] <= 900) \
                    or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_l):  # Смена хода как бы, то есть заморожены плиты или нет
                if PLAYER_TURN:
                    PLAYER_TURN = False
                    # count1 += abs(player.get_coord()[1] - 900 + coord)
                else:
                    PLAYER_TURN = True
                    # count1 += abs(player.get_coord()[1] - 900 + coord)

        if pygame.sprite.spritecollide(player, tele_group, False):  # Переход на новый уровень
            count1 = help_count_len
            PLAYER_TURN = False
            all_sprites.empty()
            tiles_group.empty()
            player_group.empty()
            tele_group.empty()
            lava_group.empty()
            kill_group.empty()
            good_blocks.empty()
            all_sprites = pygame.sprite.Group()
            tiles_group = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            main_game()
        SCREEN.blit(fon, (0, 0))
        SCREEN.blit(hat, (0, 0))
        help_count_len = (START_HEIGHT - player.rect.y) // 60 + count1
        show_current_records(help_count_len)
        show_coins(count2)
        player.move(pygame.sprite.spritecollide(player, tiles_group, False))
        if PLAYER_TURN:  # Если заморожены или наоборот происходит разное
            all_sprites.draw(SCREEN)
            SCREEN.blit(fon1, (0, 0))
            SCREEN.blit(hat, (0, 0))
            SCREEN.blit(clc, (430, 790))
        else:
            player.update(pygame.sprite.spritecollide(player, tiles_group, False))
            good_blocks.update()
            kill_group.update()
            lava_group.update()
            all_sprites.draw(SCREEN)
            SCREEN.blit(clc1, (430, 790))
        if pygame.sprite.spritecollide(player, lava_group, False):  # <--- Это закомменчено т к изза него скорее всего вылетает внезапная смерть, а вообще это должна быть смерть от лавы
            # print(3)
            all_sprites.empty()
            tiles_group.empty()
            player_group.empty()
            tele_group.empty()
            lava_group.empty()
            kill_group.empty()
            good_blocks.empty()
            CONNECTION.add_money(count2)
            CONNECTION.check_record(help_count_len)
            return end(help_count_len)
        if player.get_coord()[1] > 950: # Смерть при падении
            print(1)
            all_sprites.empty()
            tiles_group.empty()
            player_group.empty()
            tele_group.empty()
            lava_group.empty()
            kill_group.empty()
            good_blocks.empty()
            CONNECTION.add_money(count2)
            CONNECTION.check_record(help_count_len)
            return end(help_count_len)
        if pygame.sprite.spritecollide(player, kill_group, False):  # Смерть от плит-убийц
            print(2)
            all_sprites.empty()
            tiles_group.empty()
            player_group.empty()
            tele_group.empty()
            lava_group.empty()
            kill_group.empty()
            good_blocks.empty()
            CONNECTION.add_money(count2)
            CONNECTION.check_record(help_count_len)
            return end(help_count_len)
        if pygame.sprite.spritecollide(player, coin, True):  # Считаем коины
            count2 += 1
        # print(help_count_len)
        CLOCK.tick(FPS)
        pygame.display.flip()
        # print(count)


if __name__ == '__main__':
    pygame.init()
    registration_screen()
