from main import *
from help_files.configure import *

# Класс условной лавы. Она поднимается с определенной скоростью снизу, заставляя игрока  думать быстрее
class Lava(pygame.sprite.Sprite):
    image = load_image("lava1.png")
    image1 = load_image("lava2.png")
    flag = True
    count = 0

    def __init__(self, lava_group, all_sprites):
        super().__init__(lava_group, all_sprites)
        self.image = Lava.image1
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 2400
        self.check_x = 1
        self.vx = 60
        self.image = Lava.image1
        lava_group.add(self)
        all_sprites.add(self)

    def update(self, *args, **kwargs) -> None:
        self.rect.y -= self.vx / FPS