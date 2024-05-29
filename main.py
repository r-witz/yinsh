import pygame
from src.game import Game

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN|pygame.SCALED)
	pygame.display.set_caption("YINSH")
	Game("Local", "Normal").run(screen)