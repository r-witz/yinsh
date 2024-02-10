import pygame
from sys import exit

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((2560, 1440), pygame.FULLSCREEN | pygame.SCALED)
		pygame.display.set_caption('Yinsh')
		self.clock = pygame.time.Clock()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit(0)
  
			dt = self.clock.tick() / 1000
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()