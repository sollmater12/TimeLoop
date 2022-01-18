import random
from configure import *

# Класс плиты, которая перемещает на следующий уровень
class Teleport(pygame.sprite.Sprite):
    image = load_image("tile1.png")

    def __init__(self, fls, tele_group, good_blocks, all_sprites):
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
        tele_group.add(self)
        good_blocks.add(self)
        all_sprites.add(self)

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
