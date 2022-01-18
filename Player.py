from main import *
from configure import *

# Класс персонажа
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, player_group, all_sprites):
        global START_HEIGHT
        super(Player, self).__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(load_image('player.png'), (25, 43))
        # print(x)
        # print(y)
        self.rect = self.image.get_rect()
        self.pos = vec(x + 15, y - 35)
        START_HEIGHT = y - 35
        self.vel = vec(0, 0)
        self.acc = vec(0, 0.5)
        # print(self.pos[0])
        # print(self.pos[1])
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        self.isJump = False
        player_group.add(self)
        all_sprites.add(self)

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

    def jump(self, tiles_group):
        hits = pygame.sprite.spritecollide(self, tiles_group, False)
        if hits:
            self.vel.y = -4
