import pygame
from src.menu import Introduction

if __name__ == '__main__':
	pygame.init()
	pygame.font.init()
	Introduction().intro()