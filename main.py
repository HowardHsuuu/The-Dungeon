import sys
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from controllers.game_controller import GameController

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("The Dungeon")

    controller = GameController(screen)
    controller.run()

if __name__ == "__main__":
    main()
