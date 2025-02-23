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
        from config import FIST_IMAGE_PATH  # Avoid circular imports
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
        self.timer += 1
        if self.timer >= self.lifetime:
            self.kill()
        else:
            self.rect.x += int(self.direction.x * self.speed)
            self.rect.y += int(self.direction.y * self.speed)
            # Fist passes through walls; no collision check here.

class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos, direction, wall_group):
        super().__init__()
        self.direction = direction.normalize()
        # Adjust arrow size
        self.speed = FIST_SPEED * 2.5  # Faster arrow speed
        self.wall_group = wall_group
        self.image = load_image("assets/arrow.png", (PLAYER_SIZE//2, PLAYER_SIZE//4))
        # Rotate arrow to point in the movement direction
        angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
        self.image = pygame.transform.rotate(self.image, angle)
        self.image.set_colorkey((40,40,40))
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.x += int(self.direction.x * self.speed)
        self.rect.y += int(self.direction.y * self.speed)
        # Arrow cannot pass through walls – check for collisions
        for wall in self.wall_group:
            if self.rect.colliderect(wall.rect):
                self.kill()
                break
