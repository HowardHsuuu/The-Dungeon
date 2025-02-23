import math
import os

# ====================
# Image settings
# ====================
PLAYER_IMAGE_PATH = "assets/player.png"
PLAYER_KNOCKBACK_IMAGE_PATH = "assets/player-knockback.png"
MONSTER_IMAGE_PATH = "assets/monster.png"
FIST_IMAGE_PATH = "assets/attack.png"
KEY_IMAGE_PATH = "assets/key.png"
ENDPOINT_IMAGE_PATH = "assets/treasure.png"
POWERUP_IMAGE_PATH = "assets/food.png"
BACKGROUND_IMAGE_PATH = "assets/background.png"
WALL_IMAGE_PATH = "assets/wall.png"
WALL_H_IMAGE_PATH = "assets/wall-h.png"
HEART_IMAGE_PATH = "assets/heart.png"
NO_KEY_IMAGE_PATH = "assets/no-key.png"
POWERUP_ICON_IMAGE_PATH = "assets/power-up.png"

# ====================
# Adjustable parameters
# ====================
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 540
FPS = 60

# Maze parameters
MAZE_CELL_SIZE = 90
MAZE_ROWS = SCREEN_HEIGHT // MAZE_CELL_SIZE
MAZE_COLS = 30
WALL_THICKNESS = 12

WORLD_WIDTH = MAZE_COLS * MAZE_CELL_SIZE
WORLD_HEIGHT = MAZE_ROWS * MAZE_CELL_SIZE

# Player parameters
PLAYER_SPEED = 3
PLAYER_LIVES = 20
INVULN_TIME = FPS
PLAYER_SIZE = 40
KNOCKBACK_DISTANCE = 40
KNOCKBACK_SPEED = 2
KNOCKBACK_DURATION = int(KNOCKBACK_DISTANCE / KNOCKBACK_SPEED)

# Attack parameters
FIST_SPEED = 5
FIST_LIFETIME = 5
FIST_WIDTH = 20
FIST_LENGTH = 30
FIST_THROUGH_WALLS = True

# Monster parameters
MONSTER_SPEED = 1
MONSTER_SIZE = 40
NUM_MONSTERS_INIT = 10
MONSTER_SPAWN_INTERVAL = 180
MONSTER_WALK_FRAMES = 8
MONSTER_ANIM_SPEED = 0.1

# Knockback for monsters
MONSTER_KNOCKBACK_IMAGE_PATH = "assets/monster-knockback.png"
MONSTER_KNOCKBACK_DURATION = 15

# Item parameters
POWERUP_SPAWN_INTERVAL = 300
POWERUP_DURATION = 300
ATTACK_RANGE_BOOST = 10

# Key mechanics
KEY_DROP_PROBABILITY = 0.2

# Color definitions (fallback if images are not used)
COLOR_BG = (200, 200, 200)
COLOR_WALL = (0, 0, 0)
COLOR_PLAYER = (0, 0, 255)
COLOR_PLAYER_HIT = (255, 255, 0)
COLOR_MONSTER = (255, 0, 0)
COLOR_KEY = (255, 215, 0)
COLOR_ENDPOINT = (160, 82, 45)
COLOR_POWERUP = (0, 255, 0)
