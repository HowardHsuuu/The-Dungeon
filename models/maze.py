import random
import pygame
from config import MAZE_ROWS, MAZE_COLS, MAZE_CELL_SIZE, WALL_THICKNESS, COLOR_WALL
from helper import load_image
from config import WALL_IMAGE_PATH, WALL_H_IMAGE_PATH

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        if WALL_IMAGE_PATH is not None:
            self.image = load_image(WALL_IMAGE_PATH, (w, h))
            # If horizontal wall and an alternate image is provided, use it
            if w > h and WALL_H_IMAGE_PATH is not None:
                self.image = load_image(WALL_H_IMAGE_PATH, (w, h + 10))
                self.image.set_colorkey((40, 40, 40))
        else:
            self.image = pygame.Surface((w, h))
            self.image.fill(COLOR_WALL)
        self.rect = self.image.get_rect(topleft=(x, y))

def generate_maze(cols, rows):
    """
    Generate maze structure using depth-first search (DFS).
    Each cell is represented by a dictionary with visited and walls (top, right, bottom, left) flags.
    """
    maze = [[{'visited': False, 'walls': [True, True, True, True]} for _ in range(cols)] for _ in range(rows)]
    
    def carve(cx, cy):
        maze[cy][cx]['visited'] = True
        # Directions: (dx, dy, wall index)
        directions = [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]
        random.shuffle(directions)
        for dx, dy, wall in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows and not maze[ny][nx]['visited']:
                maze[cy][cx]['walls'][wall] = False
                opp = {0:2, 1:3, 2:0, 3:1}[wall]
                maze[ny][nx]['walls'][opp] = False
                carve(nx, ny)
    carve(0, 0)
    return maze

def generate_maze_walls(maze):
    """
    Create wall sprites based on the maze structure.
    """
    walls = pygame.sprite.Group()
    for row in range(MAZE_ROWS):
        for col in range(MAZE_COLS):
            cell_x = col * MAZE_CELL_SIZE
            cell_y = row * MAZE_CELL_SIZE
            cell = maze[row][col]
            # Top wall
            if cell['walls'][0]:
                walls.add(Wall(cell_x, cell_y, MAZE_CELL_SIZE, WALL_THICKNESS))
            # Right wall (only for the last column)
            if cell['walls'][1] and col == MAZE_COLS - 1:
                walls.add(Wall(cell_x + MAZE_CELL_SIZE - WALL_THICKNESS, cell_y, WALL_THICKNESS, MAZE_CELL_SIZE))
            # Bottom wall (only for the last row)
            if cell['walls'][2] and row == MAZE_ROWS - 1:
                walls.add(Wall(cell_x, cell_y + MAZE_CELL_SIZE - WALL_THICKNESS, MAZE_CELL_SIZE, WALL_THICKNESS))
            # Left wall
            if cell['walls'][3]:
                walls.add(Wall(cell_x, cell_y, WALL_THICKNESS, MAZE_CELL_SIZE))
    return walls
