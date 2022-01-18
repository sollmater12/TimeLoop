import random
import time

import Coin
import Field
import Killer
import Lava
import Player
import Teleport
from database_connect import Connection
from input_box import InputBox
from show_text_labels import *

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (750, 30)  # Задаем константы
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

CONNECTION = Connection()
CLOCK = pygame.time.Clock()
count_distance = 0  # Счетчик расстояния будет
count_money = 0  # Счетчик монет
COORDS = 0
PLAYER_TURN = False


# Функция "убийства" программы
def terminate():
    pygame.quit()
    CONNECTION.connection.close()
    sys.exit()


def refresh_data():
    global all_sprites, tiles_group, player_group, coin, kill_group, tele_group, count_distance, count_money, lava_group, PLAYER_TURN, good_blocks
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
    good_blocks = pygame.sprite.Group()
    PLAYER_TURN = False
    count_distance = 0
    count_money = 0


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


# Механика работы кнопок в главном меню плюс микро-пасхалочка
def start_screen():
    SCREEN = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('TimeLoop')
    show_start_label()
    show_records(CONNECTION)
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
                show_records(CONNECTION)
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
                show_records(CONNECTION)
                SCREEN.blit(start_label, (200, 300))
                SCREEN.blit(start_label2, (200, 450))
                pygame.display.flip()
                time.sleep(0.5)
                return support_screen()
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
    global all_sprites, tiles_group, lava_group, player_group, tele_group, kill_group, PLAYER_TURN, count, count_distance, count_money
    CONNECTION.add_money(count_distance)
    CONNECTION.check_record(help_count_len)
    running = True
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH_2, HEIGHT_2))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and 120 <= event.pos[0] <= 180 and 400 <= event.pos[1] <= 465:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and 205 <= event.pos[0] <= 275 and 400 <= event.pos[1] <= 465:
                running = False
                refresh_data()
                main_game()
            if event.type == pygame.MOUSEBUTTONDOWN and 290 <= event.pos[0] <= 370 and 400 <= event.pos[1] <= 465:
                running = False
                refresh_data()
                start_screen()


# Экран смерти - то есть при проигрыше
def end(help_count_len):
    global count_money
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
                CONNECTION.add_money(count_money)
                CONNECTION.check_record(help_count_len)
                refresh_data()
                return main_game()
            if event.type == pygame.MOUSEBUTTONDOWN and 255 <= event.pos[0] <= 340 and 370 <= event.pos[1] <= 450:
                running = False
                CONNECTION.add_money(count_money)
                CONNECTION.check_record(help_count_len)
                refresh_data()
                return start_screen()


# Функция работы основной игры
def main_game():
    global PLAYER_TURN, all_sprites, tiles_group, player_group, coin, kill_group, tele_group, count_distance, count_money, COORDS
    SCREEN = pygame.display.set_mode(SIZE_2)
    help_count_len = 0
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    hat = load_image('hat.png')
    fon1 = load_image('fon1.png')
    hat1 = load_image('hat1.png')
    clc = pygame.transform.scale(load_image('clc.png'), (74, 109))
    clc1 = pygame.transform.scale(load_image('clc1.png'), (74, 109))
    hat0 = load_image('hat0.png')
    SCREEN.blit(hat, (50, 50))
    SCREEN.blit(clc, (430, 790))  # Вплоть до сюда рисуем элементы интерфейса
    fls = []  # Список с координатами плит
    for i in range(12):  # Генерация плит
        if i == 11:
            field = Teleport.Teleport(fls, tele_group, good_blocks, all_sprites)
            tele_group.add(field)
            good_blocks.add(field)
            fls = field.ret_fls()
        if i == 0:
            field = Field.Field(fls, tiles_group, good_blocks, all_sprites)
            COORDS = field.first_coords()
            tiles_group.add(field)
            good_blocks.add(field)
            fls = field.ret_fls()
        else:
            field = Field.Field(fls, tiles_group, good_blocks, all_sprites)
            tiles_group.add(field)
            good_blocks.add(field)
            fls = field.ret_fls()
    num = random.randint(1, 3)
    if num == 1:
        kill = Killer.Killer(kill_group, all_sprites, good_blocks, player_group)
    elif num == 2:
        kill = Killer.Killer(kill_group, all_sprites, good_blocks, player_group)
        kill = Killer.Killer(kill_group, all_sprites, good_blocks, player_group)
    else:
        kill = Killer.Killer(kill_group, all_sprites, good_blocks, player_group)
        kill = Killer.Killer(kill_group, all_sprites, good_blocks, player_group)
        kill = Killer.Killer(kill_group, all_sprites, good_blocks, player_group)
    lava = Lava.Lava(lava_group, all_sprites)
    x, y = COORDS
    player = Player.Player(x, y, player_group, all_sprites)
    cn = Coin.Coin(coin, all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Прыжок перса
                    if PLAYER_TURN:
                        player.isJump = True
                        player.jump(tiles_group)
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
            count_distance = help_count_len
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
        if (START_HEIGHT - player.rect.y) // 60 + count_distance >= help_count_len:
            help_count_len = (START_HEIGHT - player.rect.y) // 60 + count_distance
        show_current_records(help_count_len)
        show_coins(count_money)
        player.move(pygame.sprite.spritecollide(player, tiles_group, False))
        if PLAYER_TURN:  # Если заморожены или наоборот происходит разное
            all_sprites.draw(SCREEN)
            SCREEN.blit(fon1, (0, 0))
            SCREEN.blit(hat, (0, 0))
            SCREEN.blit(clc, (430, 790))
        else:
            check = pygame.sprite.spritecollide(player, tiles_group, False)
            player.update(check)
            # tiles_group.update()
            good_blocks.update()
            kill_group.update()
            lava_group.update()
            all_sprites.draw(SCREEN)
            SCREEN.blit(clc1, (430, 790))
        if pygame.sprite.spritecollide(player, lava_group,
                                       False):  # <--- Это закомменчено т к изза него скорее всего вылетает внезапная смерть, а вообще это должна быть смерть от лавы
            return end(help_count_len)
        if player.get_coord()[1] > 950:  # Смерть при падении
            return end(help_count_len)
        if pygame.sprite.spritecollide(player, kill_group, False):  # Смерть от плит-убийц
            return end(help_count_len)
        if pygame.sprite.spritecollide(player, coin, True):  # Считаем коины
            count_money += 1
        CLOCK.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    print(1)
    pygame.init()
    registration_screen()

