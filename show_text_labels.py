from main import *

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
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color(0, 0, 0))
    SCREEN.blit(string_rendered, (180, 200))


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