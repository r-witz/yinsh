import pygame
from src.game import Game
from src.scan import scan_network
from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
	ip_serv = scan_network()[0]
	pygame.init()
	screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN|pygame.SCALED)
	pygame.display.set_caption("YINSH")
	Game("Online", "Normal", ip_serv).run(screen)