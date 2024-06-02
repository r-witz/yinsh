import pygame
import threading
from socket import gethostbyname, gethostname
from src.game import Game
from src.server import Server

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN|pygame.SCALED)
	pygame.display.set_caption("YINSH")
	threading.Thread(target=Server().start_server, args=()).start()
	Game("Online", "Normal", gethostbyname(gethostname())).run(screen)