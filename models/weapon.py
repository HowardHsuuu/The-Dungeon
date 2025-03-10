import math
import pygame
from config import PLAYER_SIZE, FIST_SPEED
from helper import load_image

class Fist(pygame.sprite.Sprite):
    def __init__(self, player, wall_group):
        super().__init__()
        self.player = player
        self.direction = player.direction.copy()
        self.speed = FIST_SPEED
        self.lifetime = 5 + player.attack_range_boost
        self.width = 20 + player.attack_range_boost
        self.length = 30 + player.attack_range_boost
        self.wall_group = wall_group
        from config import FIST_IMAGE_PATH
        if FIST_IMAGE_PATH:
            self.original_image = load_image(FIST_IMAGE_PATH, (self.width, self.length))
        else:
            self.original_image = pygame.Surface((self.width, self.length))
            self.original_image.fill((255,255,255))
        angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.image.set_colorkey((40,40,40))
        offset_distance = PLAYER_SIZE / 3
        offset_vector = self.direction * offset_distance
        self.rect = self.image.get_rect(center=(player.rect.centerx + offset_vector.x,
                                                 player.rect.centery + offset_vector.y))
        self.timer = 0

    def update(self):
        # TODO: 讓勇者的拳擊變強！
        '''
        拳擊物件的邏輯：當空白鍵被按時，一個 Fist 物件會被加入，並且在每個 frame 呼叫一次 update()
        發射物件（拳頭）的管理方式是：self.lifetime 作為拳頭存在的時間，用 self.timer 來計時
        self.speed 是拳頭的移動速度
        self.direction 是拳頭的移動方向 (self.direction.x, self.direction.y)
        你可以透過修改 self.rect.x, self.rect.y 來移動拳頭
        '''
        # ---------------- your code starts here ----------------
        self.kill() #刪除物件
        # ---------------- your code ends here ------------------

class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos, direction, wall_group):
        super().__init__()
        self.direction = direction.normalize()
        self.speed = FIST_SPEED * 2.5
        self.wall_group = wall_group
        self.image = load_image("assets/arrow.png", (PLAYER_SIZE//2, PLAYER_SIZE//4))
        angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
        self.image = pygame.transform.rotate(self.image, angle)
        self.image.set_colorkey((40,40,40))
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        # TODO: 修好勇者的弓箭
        '''
        邏輯和拳頭大致相同，但弓箭沒有 lifetime，可以一直飛行直到碰撞到牆壁
        self.rect.colliderect(wall.rect) 可以檢查弓箭是否碰撞到「某個」牆壁
        self.wall_group 是所有牆壁的群組，是 iterable 的
        '''
        # ---------------- your code starts here ----------------
        self.kill() #刪除物件
        # ---------------- your code ends here ------------------
