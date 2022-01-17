from help_files.configure import *
from main import *


# Класс тайлов, по которым прыгает перс
class Field(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('check_draw.png'), (50, 13))

    def __init__(self, fls, tiles_group, good_blocks, all_sprites):
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
            self.FIRST_X = self.rect.x
            self.FIRST_Y = self.rect.y
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
        self.vx = random.choice([60, 120,
                                 180])  # Этот параметр отвечает за скорость. Если его менять, то плиты останавливаются в конце экрана
        self.image = Field.image
        tiles_group.add(self)
        good_blocks.add(self)
        all_sprites.add(self)

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

    def first_coords(self):
        return self.FIRST_X, self.FIRST_Y
