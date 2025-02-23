import pygame

def load_image(path, size):
    """Load and scale an image, and set the colorkey for transparency."""
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, size)
    image.set_colorkey((40, 40, 40))
    return image
