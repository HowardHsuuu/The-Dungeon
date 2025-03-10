import pygame
from config import (
    PLAYER_IMAGE_PATH, PLAYER_KNOCKBACK_IMAGE_PATH,
    PLAYER_SIZE, PLAYER_LIVES, PLAYER_SPEED,
    COLOR_PLAYER, COLOR_PLAYER_HIT,
    WORLD_WIDTH, WORLD_HEIGHT, FPS,
    KNOCKBACK_SPEED, KNOCKBACK_DURATION
)
from helper import load_image

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        if PLAYER_IMAGE_PATH:
            self.normal_image = load_image(PLAYER_IMAGE_PATH, (PLAYER_SIZE, PLAYER_SIZE))
        else:
            self.normal_image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
            self.normal_image.fill(COLOR_PLAYER)
        if PLAYER_KNOCKBACK_IMAGE_PATH:
            self.knockback_image = load_image(PLAYER_KNOCKBACK_IMAGE_PATH, (PLAYER_SIZE, PLAYER_SIZE))
        else:
            self.knockback_image = None
        self.image = self.normal_image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.lives = PLAYER_LIVES
        self.invuln_timer = 0
        self.direction = pygame.math.Vector2(1, 0)
        self.last_horizontal = 1
        self.powerup_timer = 0
        self.attack_range_boost = 0
        self.knockback_timer = 0
        self.knockback_vel = pygame.math.Vector2(0, 0)
        self.has_key = False
        self.has_bow = False
        self.is_attacking = False
        self.attack_frames = []
        for i in range(1, 10):
            frame_path = f"assets/player-attack/{i}.png"
            if i == 8:
                frame_img = load_image(frame_path, (PLAYER_SIZE+20, PLAYER_SIZE))
            else:
                frame_img = load_image(frame_path, (PLAYER_SIZE, PLAYER_SIZE))
            self.attack_frames.append(frame_img)
        self.attack_anim_index = 0
        self.attack_anim_speed = 0.2
        self.arrow_spawned = False
        self.rapid_fire = False

        self.walk_frames = []
        for i in range(1, 9):
            frame_path = f"assets/player-walk/{i}.png"
            frame_img = load_image(frame_path, (PLAYER_SIZE, PLAYER_SIZE))
            self.walk_frames.append(frame_img)
        self.current_frame = 0
        self.animation_speed = 0.2

    def update(self, walls):
        if self.knockback_timer > 0: # 玩家角色被擊退
            if self.knockback_image:
                self.image = self.knockback_image.copy()
            else:
                self.image.fill(COLOR_PLAYER_HIT)
            old_x = self.rect.x
            self.rect.x += int(self.knockback_vel.x)
            if any(self.rect.colliderect(w.rect) for w in walls):
                self.rect.x = old_x
            old_y = self.rect.y
            self.rect.y += int(self.knockback_vel.y)
            if any(self.rect.colliderect(w.rect) for w in walls):
                self.rect.y = old_y
            self.knockback_timer -= 1
        elif self.is_attacking: # 角色攻擊中（弓箭）
            self.attack_anim_index += self.attack_anim_speed
            if self.attack_anim_index >= len(self.attack_frames):
                self.is_attacking = False
                self.attack_anim_index = 0
                self.arrow_spawned = False
                self.image = self.normal_image.copy()
            else:
                new_image = self.attack_frames[int(self.attack_anim_index)]
                if self.last_horizontal < 0:
                    new_image = pygame.transform.flip(new_image, True, False)
                    new_image.set_colorkey((40,40,40))
                self.image = new_image
        else: # 角色沒有在攻擊也沒有被擊退，可以移動
            keys = pygame.key.get_pressed()
            dx = dy = 0
            # TODO: 讓勇者動起來！
            '''
            keys 為一個 list，裡面包含了所有按鍵的狀態，按鍵為 True，沒按則為 False
            例如 keys[pygame.K_LEFT] 會回傳 True 或 False，表示左鍵有沒有被按下
            dx, dy 為勇者的移動方向，分別為 x 軸和 y 軸的移動速度
            PLAYER_SPEED 為 config.py 中設定勇者的移動速度
            '''
            # ---------------- your code starts here ----------------
            # Hint: 判斷 dx, dy 的值應該指定成什麼
            # ---------------- your code ends here ----------------

            if dx != 0 or dy != 0:
                if dx != 0:
                    self.last_horizontal = 1 if dx > 0 else -1
                self.direction = pygame.math.Vector2(dx, dy).normalize()
                self.current_frame += self.animation_speed
                if self.current_frame >= len(self.walk_frames):
                    self.current_frame = 0
                new_image = self.walk_frames[int(self.current_frame)]
                if self.last_horizontal < 0:
                    new_image = pygame.transform.flip(new_image, True, False)
                    new_image.set_colorkey((40,40,40))
                self.image = new_image
            else:
                if self.last_horizontal < 0:
                    self.image = pygame.transform.flip(self.normal_image, True, False)
                    self.image.set_colorkey((40,40,40))
                else:
                    self.image = self.normal_image.copy()
                self.current_frame = 0

            self.rect.x += dx
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dx > 0:
                        self.rect.right = wall.rect.left
                    elif dx < 0:
                        self.rect.left = wall.rect.right
            self.rect.y += dy
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dy > 0:
                        self.rect.bottom = wall.rect.top
                    elif dy < 0:
                        self.rect.top = wall.rect.bottom

            self.rect.left = max(0, self.rect.left)
            self.rect.top = max(0, self.rect.top)
            self.rect.right = min(WORLD_WIDTH, self.rect.right)
            self.rect.bottom = min(WORLD_HEIGHT, self.rect.bottom)

        if self.invuln_timer > 0:
            self.invuln_timer -= 1
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer == 0:
                self.attack_range_boost = 0
                self.rapid_fire = False

    def start_knockback(self, knockback_velocity, duration):
        self.knockback_vel = knockback_velocity
        self.knockback_timer = duration

    def start_arrow_attack(self):
        if self.has_bow and not self.is_attacking:
            self.is_attacking = True
            self.attack_anim_index = 0
            self.arrow_spawned = False
