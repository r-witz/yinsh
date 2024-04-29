import pygame # type: ignore
from sys import exit
from math import sqrt

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN|pygame.SCALED)
pygame.display.set_caption("YINSH")

class Hexagone:
    def __init__(self, x, y, size, q, r):
        self.x = x
        self.y = y

        self.center = (x, y)
        self.size = size
        self.width = sqrt(3)*size
        self.height = 2*size

        self.positions = [
            (self.x, self.y - self.height/2),
            (self.x + self.width/2, self.y - self.height/4),
            (self.x + self.width/2, self.y + self.height/4),
            (self.x, self.y + self.height/2),
            (self.x - self.width/2, self.y + self.height/4),
            (self.x - self.width/2, self.y - self.height/4)
        ]

        self.q = q
        self.r = r
        self.s = -q - r

    def draw(self, surface):
        pygame.draw.polygon(surface, (0, 0, 0), [(self.x+self.positions[k][0], self.y+self.positions[k][1]) for k in range(6)], 3)

class Board:
    def __init__(self):
        self.board = [
            [None, None, None, None, None, None, 1, 1, 1, 1, None],
            [None, None, None, None, 1, 1, 1, 1, 1, 1, 1],
            [None, None, None, 1, 1, 1, 1, 1, 1, 1, 1],
            [None, None, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [None, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [None, 1, 1, 1, 1, 1, 1, 1, 1, 1, None],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, None],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, None, None],
            [1, 1, 1, 1, 1, 1, 1, 1, None, None, None],
            [1, 1, 1, 1, 1, 1, 1, None, None, None, None],
            [None, 1, 1, 1, 1, None, None, None, None, None, None]
        ]

        self.init_board()

    def init_board(self):
        size = 100
        horiz = sqrt(3)*size/2
        vert = 3/2*size

        startx, starty = -100, 150
        x, y = startx, starty

        for i in range(11):
            for j in range(11):
                if self.board[i][j] == 1:
                    q = j-5
                    r = i-5
                    self.board[i][j] = Hexagone(x, y, size, q, r)
                x += horiz
            x = startx + horiz/2
            y = starty + vert/2
            startx = x
            starty = y

    def get_neighbours(self, i, j):
        vector = [
            (-1, 0),
            (-1, 1),
            (0, 1), 
            (1, 0),
            (1, -1),
            (0, -1) 
        ]

        neighbours_coords = []

        for y, x in vector:
            if 0 <= i+y < 11 and 0 <= j+x < 11 and self.board[i+y][j+x] != None:
                neighbours_coords.append((i+y, j+x))
        return neighbours_coords
    
    def draw(self):
        surface = pygame.Surface((1080, 1080), pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()

        for i in range(11):
            for j in range(11):
                if self.board[i][j] != None:
                    x, y = self.board[i][j].center
                    neighbours = self.get_neighbours(i, j)
                    for neighbour in neighbours:
                        nx, ny = self.board[neighbour[0]][neighbour[1]].center
                        pygame.draw.line(surface, (0, 0, 0), (x, y), (nx, ny), 3)

        surface = pygame.transform.rotate(surface, -90)
        return surface

    def update(self):
        pass

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.board = Board()

    def run(self):
        run = True

        while run:
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False
                    pygame.quit()
                    exit()

            surface_board = self.board.draw()
            self.screen.blit(surface_board, (420, 0))

            self.clock.tick(60)
            pygame.display.flip()

if __name__ == "__main__":
    Game(screen).run()