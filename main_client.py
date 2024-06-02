import pygame
from socket import gethostbyname, gethostname
from src.game import Game

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN|pygame.SCALED)
	pygame.display.set_caption("YINSH")
	Game("Online", "Normal", gethostbyname(gethostname())).run(screen)