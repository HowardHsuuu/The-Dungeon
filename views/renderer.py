import os
import random
import pygame
from helper import load_image
from config import WORLD_WIDTH, WORLD_HEIGHT
from models.item import Endpoint

class Renderer:
    def __init__(self, screen, assets):
        self.screen = screen

        tile_paths = []
        for i in range(1, 6):
            path = f"assets/tiles{i}.png"
            if os.path.exists(path):
                tile_paths.append(path)
        if tile_paths:
            self.tile_images = [load_image(path, (128, 100)) for path in tile_paths]
            self.tile_width = self.tile_images[0].get_width()
            self.tile_height = self.tile_images[0].get_height()
            self.tiled_background = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
            for x in range(0, WORLD_WIDTH, self.tile_width):
                for y in range(0, WORLD_HEIGHT, self.tile_height):
                    tile = random.choice(self.tile_images)
                    self.tiled_background.blit(tile, (x, y))
            self.background_image = self.tiled_background
        else:
            self.background_image = assets.get('background')

        self.heart_image = assets.get('heart')
        self.no_key_icon = assets.get('no_key')
        self.key_icon = assets.get('key')
        self.powerup_icon = assets.get('powerup')
        self.bg_color = assets.get('bg_color', (0, 0, 0))
        self.arrow_icon = load_image("assets/arrow-icon.png", (30, 30))
        self.no_key_icon = load_image("assets/no-key.png", (25, 35))

    def render(self, all_sprites, wall_group, player, endpoint_group, camera_x,
               game_over, win, endpoint_message, font, title_font):
        if self.background_image:
            self.screen.blit(self.background_image, (-camera_x, 0))
        else:
            self.screen.fill(self.bg_color)
        for wall in wall_group:
            self.screen.blit(wall.image, (wall.rect.x - camera_x, wall.rect.y))
        for endpoint in endpoint_group:
            self.screen.blit(endpoint.image, (endpoint.rect.x - camera_x, endpoint.rect.y))
        for sprite in all_sprites:
            if not isinstance(sprite, Endpoint):
                self.screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
        if endpoint_message:
            msg = title_font.render(endpoint_message, True, (255, 0, 0))
            msg_rect = msg.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(msg, msg_rect)
        if game_over:
            msg = title_font.render("GAME OVER", True, (255, 0, 0))
            msg_rect = msg.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
            self.screen.blit(msg, msg_rect)
            msg = font.render("Press R to restart", True, (255, 0, 0))
            msg_rect = msg.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 10))
            self.screen.blit(msg, msg_rect)
        elif win:
            msg = title_font.render("YOU WIN!", True, (0, 255, 0))
            msg_rect = msg.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
            self.screen.blit(msg, msg_rect)
            msg = font.render("Press R to restart", True, (0, 255, 0))
            msg_rect = msg.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 10))
            self.screen.blit(msg, msg_rect)
        # TODO 5: 顯示勇者狀態
        '''
        模仿 demo 中看到的顯示方式，或是你喜歡的表現方式
        self.heart_image 為一個愛心的圖案，你可以用 self.screen.blit(self.heart_image, (x, y)) 來將它顯示在畫面上 (x, y) 處
        player.lives 可以取得勇者的生命值
        player.has_key 可以取得勇者是否有鑰匙 --> 沒有鑰匙時顯示 self.no_key_icon, 有鑰匙時顯示 self.key_icon
        player.has_bow 可以取得勇者是否有弓箭 --> 沒有弓箭時不顯示，有弓箭時顯示 self.arrow_icon
        player.powerup_timer 可以取得勇者的道具效果剩餘時間 --> 有道具效果時顯示 self.powerup_icon，並在顯示效果剩餘時間
        '''
        # ---------------- your code starts here ----------------
        # Hint: 在畫生命值時，或許可以考慮使用迴圈，並且請記得
        # ---------------- your code ends here ------------------

        center = pygame.math.Vector2(player.rect.centerx - camera_x, player.rect.centery)
        player_size = player.image.get_width()
        offset_distance = player_size / 2
        D = player.direction.normalize()
        start_point = center + D * offset_distance
        arrow_line_length = 10
        end_point = start_point + D * arrow_line_length
        arrow_head_length = 5
        arrow_head_width = 8
        tip = end_point + D * arrow_head_length
        perp = pygame.math.Vector2(-D.y, D.x)
        base_left = end_point - D * arrow_head_length + perp * (arrow_head_width / 2)
        base_right = end_point - D * arrow_head_length - perp * (arrow_head_width / 2)
        arrow_color = (255, 0, 0)
        pygame.draw.line(self.screen, arrow_color, start_point, end_point, 3)
        pygame.draw.polygon(self.screen, arrow_color, [tip, base_left, base_right])
