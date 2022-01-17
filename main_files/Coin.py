from main import *
from help_files.configure import load_image

# Класс монетки, которую надо собирать, но еще счетчки их, как и счетчик расстояния и в конечном счете рекорда, не доделан
class Coin(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('cn.png'), (50, 50))

    def __init__(self):
        global coin, all_sprites
        super().__init__(coin, all_sprites)
        self.image = Coin.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(5, 450)
        self.rect.y = random.randrange(100, 850)
        self.image = Coin.image
        coin.add(self)
        all_sprites.add(self)