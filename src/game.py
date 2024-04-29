import pygame # type: ignore
from sys import exit
from math import sqrt
import cv2 # type: ignore

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN|pygame.SCALED)
pygame.display.set_caption("YINSH")

class Hexagone:
    def __init__(self, x, y, size, q, r):
        self.center = (x, y)
        self.size = size
        self.width = 2*size
        self.height = sqrt(3)*size

        self.q = q
        self.r = r
        self.s = -q - r

        self.positions = [
            (x-size, y),
            (x-size/2, y-self.height/2),
            (x+size/2, y-self.height/2),
            (x+size, y),
            (x+size/2, y+self.height/2),
            (x-size/2, y+self.height/2)
        ]

    def contains(self, point):
        x, y = point
        return all(pygame.math.Vector2(x, y).distance_to(pygame.math.Vector2(px, py)) <= self.size*2 for px, py in self.positions)


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
        size = 48
        horiz = 3/2*size
        vert = sqrt(3)*size/2

        startx, starty = 150, -75
        x, y = startx, starty

        for i in range(11):
            for j in range(11):
                if self.board[i][j] == 1:
                    q = j-5
                    r = i-5
                    self.board[i][j] = Hexagone(x, y, size, q, r)
                x += horiz
                y += vert
            x = startx
            y = starty + vert * 2
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
    
    def get_hexagon_at_point(self, point):
        for row in self.board:
            for hexagon in row:
                if hexagon is not None and hexagon.contains(point):
                    return hexagon.q, hexagon.r, hexagon.s
        return None, None, None
    
    def draw_hexagons(self):
        surface = pygame.Surface((1080, 1080), pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()

        for i in range(11):
            for j in range(11):
                if self.board[i][j] != None:
                    x, y = self.board[i][j].center
                    size = self.board[i][j].size
                    height = self.board[i][j].height
                    pygame.draw.polygon(screen, (255, 255, 255), [
                        (x-size, y),
                        (x-size/2, y-height/2),
                        (x+size/2, y-height/2),
                        (x+size, y),
                        (x+size/2, y+height/2),
                        (x-size/2, y+height/2)
                    ], 6)

        return surface

    
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
                        pygame.draw.line(surface, (255, 255, 255), (x, y), (nx, ny), 14)

        for i in range(11):
            for j in range(11):
                if self.board[i][j] != None:
                    x, y = self.board[i][j].center
                    neighbours = self.get_neighbours(i, j)
                    for neighbour in neighbours:
                        nx, ny = self.board[neighbour[0]][neighbour[1]].center
                        pygame.draw.line(surface, (0, 0, 0), (x, y), (nx, ny), 10)

        return surface

    def update(self):
        pass

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.board = Board()

        self.video = cv2.VideoCapture("assets/graphics/background/menu.mp4")
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

    def play_video(self, surface):
        success, video_image = self.video.read()
        if not success:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, video_image = self.video.read()
        video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
        surface.blit(video_surf, (0, 0))

    def run(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    q, r, s = self.board.get_hexagon_at_point(mouse_pos)
                    print(f"Clicked hexagon coordinates: q={q}, r={r}, s={s}")

            self.clock.tick(self.fps)

            self.play_video(self.screen)
            surface_board = self.board.draw()
            self.screen.blit(surface_board, (0, 0))
            # surface_hexagons = self.board.draw_hexagons()
            # self.screen.blit(surface_hexagons, (0, 0))

            pygame.display.flip()

if __name__ == "__main__":
    Game(screen).run()