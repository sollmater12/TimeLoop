from main import *
from help_files.configure import *

# Класс плиты-убийцы. Ее касаться нельзя
class Killer(pygame.sprite.Sprite):
    image = load_image('tile_kill2.png')
    image2 = pygame.transform.scale(image, (150, 26))

    def __init__(self, kill_group, all_sprites, good_blocks, player_group):
        super().__init__(kill_group, all_sprites)
        self.image = Killer.image2
        self.rect = self.image2.get_rect()
        self.rect.x = -249
        self.rect.y = random.randrange(60, 700)
        while pygame.sprite.spritecollide(self, good_blocks, False) or pygame.sprite.spritecollide(self, player_group,
                                                                                                   False):
            self.rect.y = random.randrange(60, 880)
        direc = [-1, 1]
        self.check_x = random.choice(direc)
        self.vx = random.choice([60, 120, 180])
        self.image = Killer.image2
        kill_group.add(self)
        all_sprites.add(self)

    def update(self, *args, **kwargs) -> None:
        self.rect.x += self.vx / FPS
        if self.rect.x > 507:
            self.rect.x = -249