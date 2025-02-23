import os
import random
import pygame
from helper import load_image
from config import WORLD_WIDTH, WORLD_HEIGHT

class Renderer:
    def __init__(self, screen, assets):
        self.screen = screen

        # Check for three types of tile images
        tile_paths = []
        for i in range(1, 6):
            path = f"assets/tiles{i}.png"
            if os.path.exists(path):
                tile_paths.append(path)
        if tile_paths:
            # Load available tile images and assume a fixed size (adjust as needed)
            self.tile_images = [load_image(path, (128, 100)) for path in tile_paths]
            self.tile_width = self.tile_images[0].get_width()
            self.tile_height = self.tile_images[0].get_height()
            # Create a background surface by randomly choosing one tile for each cell
            self.tiled_background = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
            for x in range(0, WORLD_WIDTH, self.tile_width):
                for y in range(0, WORLD_HEIGHT, self.tile_height):
                    tile = random.choice(self.tile_images)
                    self.tiled_background.blit(tile, (x, y))
            self.background_image = self.tiled_background
        else:
            # Fall back to a single background image if no tile images are found.
            self.background_image = assets.get('background')

        self.heart_image = assets.get('heart')
        self.no_key_icon = assets.get('no_key')
        self.key_icon = assets.get('key')
        self.powerup_icon = assets.get('powerup')
        self.bg_color = assets.get('bg_color', (0, 0, 0))
        self.arrow_icon = load_image("assets/arrow-icon.png", (30, 30))
        # Ensure no_key_icon has the correct size and transparency
        self.no_key_icon = load_image("assets/no-key.png", (25, 35))
        
    def render(self, all_sprites, wall_group, player, endpoint_group, camera_x,
               game_over, win, endpoint_message, font, title_font):
        if self.background_image:
            self.screen.blit(self.background_image, (-camera_x, 0))
        else:
            self.screen.fill(self.bg_color)
        for wall in wall_group:
            self.screen.blit(wall.image, (wall.rect.x - camera_x, wall.rect.y))
        for sprite in all_sprites:
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
        # Top row: display hearts (lives)
        if self.heart_image:
            heart_margin_x = 10
            heart_margin_y = 10
            heart_spacing = 25
            for i in range(player.lives):
                x = self.screen.get_width() - (heart_spacing * (i + 1) + 10)
                y = heart_margin_y
                self.screen.blit(self.heart_image, (x, y))
        # Bottom row: display key, arrow, and powerup icons.
        bottom_y = 10 + (self.heart_image.get_height() if self.heart_image else 25) + 5
        icon_spacing = 40
        x_start = self.screen.get_width() - (icon_spacing * 3 + 10)
        key_to_show = self.key_icon if player.has_key else self.no_key_icon
        self.screen.blit(key_to_show, (x_start + 2 * icon_spacing, bottom_y))
        if player.has_bow:
            self.screen.blit(self.arrow_icon, (x_start + icon_spacing, bottom_y))
        if player.powerup_timer > 0:
            self.screen.blit(self.powerup_icon, (x_start, bottom_y))
            powerup_seconds = int(player.powerup_timer / 60)
            timer_text = font.render(str(powerup_seconds), True, (255, 255, 255))
            timer_rect = timer_text.get_rect(center=(x_start + self.powerup_icon.get_width() // 2,
                                                      bottom_y + self.powerup_icon.get_height() // 2))
            self.screen.blit(timer_text, timer_rect)
