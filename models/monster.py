import random
import pygame
from config import (
    MONSTER_IMAGE_PATH, MONSTER_SIZE, MONSTER_SPEED, 
    MONSTER_WALK_FRAMES, MONSTER_ANIM_SPEED,
    COLOR_MONSTER, MONSTER_KNOCKBACK_IMAGE_PATH, MONSTER_KNOCKBACK_DURATION
)
from helper import load_image

class Monster(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Load normal image
        if MONSTER_IMAGE_PATH:
            self.normal_image = load_image(MONSTER_IMAGE_PATH, (MONSTER_SIZE, MONSTER_SIZE))
        else:
            self.normal_image = pygame.Surface((MONSTER_SIZE, MONSTER_SIZE))
            self.normal_image.fill(COLOR_MONSTER)
        self.image = self.normal_image.copy()
        self.rect = self.image.get_rect(center=pos)

        # Load walking animation frames (assets/monster-walk/1.png ~ MONSTER_WALK_FRAMES.png)
        self.walk_frames = []
        for i in range(1, MONSTER_WALK_FRAMES + 1):
            frame_path = f"assets/monster-walk/{i}.png"
            frame_img = load_image(frame_path, (MONSTER_SIZE, MONSTER_SIZE))
            self.walk_frames.append(frame_img)
        self.current_frame = 0
        self.animation_speed = MONSTER_ANIM_SPEED

        # Load death animation frames (assets/monster-die/1.png ~ 4.png)
        self.death_frames = []
        for i in range(1, 5):
            frame_path = f"assets/monster-die/{i}.png"
            frame_img = load_image(frame_path, (MONSTER_SIZE, MONSTER_SIZE))
            self.death_frames.append(frame_img)
        self.death_anim_speed = 0.1
        self.death_frame_index = 0

        # Load attack animation frames (assets/monster-attack/1.png ~ 7.png)
        self.attack_frames = []
        for i in range(1, 8):
            frame_path = f"assets/monster-attack/{i}.png"
            frame_img = load_image(frame_path, (MONSTER_SIZE+5, MONSTER_SIZE+5))
            self.attack_frames.append(frame_img)
        self.attack_anim_speed = 0.1
        self.attack_frame_index = 0
        self.attack_delay = random.randint(180, 600)
        self.is_attacking = False

        # Set random movement direction
        self.velocity = pygame.math.Vector2(MONSTER_SPEED, 0).rotate(random.uniform(0, 360))

        # Health: requires two hits to kill
        self.health = 2

        # Knockback state
        self.knockback_timer = 0
        self.knockback_velocity = pygame.math.Vector2(0, 0)
        if MONSTER_KNOCKBACK_IMAGE_PATH:
            self.knockback_image = load_image(MONSTER_KNOCKBACK_IMAGE_PATH, (MONSTER_SIZE, MONSTER_SIZE))
        else:
            self.knockback_image = self.normal_image

        # Death state
        self.is_dying = False
        self.death_velocity = pygame.math.Vector2(0, 0)

    def hit(self, knockback_velocity):
        """
        Called when the monster is hit:
         - On the first hit, reduce health and apply knockback.
         - On the second hit, trigger death animation and set death velocity.
         - If the monster is attacking, interrupt the attack.
        """
        if self.is_dying:
            return

        if self.is_attacking:
            self.is_attacking = False
            self.attack_frame_index = 0
            self.attack_delay = random.randint(180, 600)
            self.velocity = pygame.math.Vector2(MONSTER_SPEED, 0).rotate(random.uniform(0, 360))

        if self.health == 2:
            self.health = 1
            self.knockback_timer = MONSTER_KNOCKBACK_DURATION
            self.knockback_velocity = knockback_velocity
            self.image = self.knockback_image.copy()
        else:
            self.is_dying = True
            self.death_frame_index = 0
            self.death_velocity = knockback_velocity

    def update(self, walls):
        if self.is_dying:
            # Death state: move using death_velocity and play death animation.
            old_x = self.rect.x
            self.rect.x += int(self.death_velocity.x)
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    self.rect.x = old_x
                    break
            old_y = self.rect.y
            self.rect.y += int(self.death_velocity.y)
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    self.rect.y = old_y
                    break

            self.death_frame_index += self.death_anim_speed
            if self.death_frame_index >= len(self.death_frames):
                self.kill()
            else:
                self.image = self.death_frames[int(self.death_frame_index)]
        elif self.knockback_timer > 0:
            # Knockback state: move using knockback_velocity.
            old_x = self.rect.x
            self.rect.x += int(self.knockback_velocity.x)
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    self.rect.x = old_x
                    break
            old_y = self.rect.y
            self.rect.y += int(self.knockback_velocity.y)
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    self.rect.y = old_y
                    break
            self.knockback_timer -= 1
            if self.knockback_timer <= 0:
                self.image = self.normal_image.copy()
        else:
            if self.is_attacking:
                self.attack_frame_index += self.attack_anim_speed
                if self.attack_frame_index >= len(self.attack_frames):
                    self.is_attacking = False
                    self.attack_frame_index = 0
                    self.attack_delay = random.randint(180, 600)
                    self.image = self.normal_image.copy()
                    self.velocity = pygame.math.Vector2(MONSTER_SPEED, 0).rotate(random.uniform(0, 360))
                else:
                    self.image = self.attack_frames[int(self.attack_frame_index)]
            else:
                self.attack_delay -= 1
                if self.attack_delay <= 0:
                    self.is_attacking = True
                    self.attack_frame_index = 0
                    self.velocity = pygame.math.Vector2(0, 0)
                else:
                    old_x = self.rect.x
                    self.rect.x += self.velocity.x
                    for wall in walls:
                        if self.rect.colliderect(wall.rect):
                            self.rect.x = old_x
                            self.velocity.x *= -1
                            break
                    old_y = self.rect.y
                    self.rect.y += self.velocity.y
                    for wall in walls:
                        if self.rect.colliderect(wall.rect):
                            self.rect.y = old_y
                            self.velocity.y *= -1
                            break

                    if self.velocity.length() > 0:
                        self.current_frame += self.animation_speed
                        if self.current_frame >= len(self.walk_frames):
                            self.current_frame = 0
                        new_image = self.walk_frames[int(self.current_frame)]
                        if self.velocity.x < 0:
                            new_image = pygame.transform.flip(new_image, True, False)
                            new_image.set_colorkey((40, 40, 40))
                        self.image = new_image
                    else:
                        self.current_frame = 0
                        self.image = self.normal_image.copy()
