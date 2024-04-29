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
        print(self.get_lines(3, 9))

    def init_board(self):
        size = 48
        horiz = 3/2*size
        vert = sqrt(3)*size/2

        startx, starty = 2*size, size/2
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
    
    def get_lines(self, i, j):
        vertical = self.get_cells_between(0, j, 10, j)
        lower_diagonal = self.get_cells_between(i, 0, i, 10)
        upper_diagonal = None
        list_diagonals = [
            ((0, 0),),
            ((1, 0), (0, 1)),
            ((2, 0), (1, 1), (0, 2)),
            ((3, 0), (2, 1), (1, 2), (0, 3)),
            ((4, 0), (3, 1), (2, 2), (1, 3), (0, 4)),
            ((5, 0), (4, 1), (3, 2), (2, 3), (1, 4), (0, 5)),
            ((6, 0), (5, 1), (4, 2), (3, 3), (2, 4), (1, 5), (0, 6)),
            ((7, 0), (6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6), (0, 7)),
            ((8, 0), (7, 1), (6, 2), (5, 3), (4, 4), (3, 5), (2, 6), (1, 7), (0, 8)),
            ((9, 0), (8, 1), (7, 2), (6, 3), (5, 4), (4, 5), (3, 6), (2, 7), (1, 8), (0, 9)),
            ((10, 0), (9, 1), (8, 2), (7, 3), (6, 4), (5, 5), (4, 6), (3, 7), (2, 8), (1, 9), (0, 10)),
            ((10, 1), (9, 2), (8, 3), (7, 4), (6, 5), (5, 6), (4, 7), (3, 8), (2, 9), (1, 10)),
            ((10, 2), (9, 3), (8, 4), (7, 5), (6, 6), (5, 7), (4, 8), (3, 9), (2, 10)),
            ((10, 3), (9, 4), (8, 5), (7, 6), (6, 7), (5, 8), (4, 9), (3, 10)),
            ((10, 4), (9, 5), (8, 6), (7, 7), (6, 8), (5, 9), (4, 10)),
            ((10, 5), (9, 6), (8, 7), (7, 8), (6, 9), (5, 10)),
            ((10, 6), (9, 7), (8, 8), (7, 9), (6, 10)),
            ((10, 7), (9, 8), (8, 9), (7, 10)),
            ((10, 8), (9, 9), (8, 10)),
            ((10, 9), (9, 10)),
            ((10, 10))
        ]
        for diagonal in list_diagonals:
            if (i, j) in diagonal:
                upper_diagonal = diagonal
                break

        return [vertical, lower_diagonal, upper_diagonal]

    def get_cells_between(self, i, j, k, l):
        if j==l:
            return [(y, j) for y in range(min(i, k), max(i, k)+1) if self.board[y][j] != None]
        elif i==k:
            return [(i, x) for x in range(min(j, l), max(j, l)+1) if self.board[i][x] != None]
        elif abs(i-k) == abs(j-l):
            return [(y, x) for y, x in zip(range(max(i, k), min(i, k), -1), range(min(j, l), max(j, l))) if self.board[y][x] != None]
        else:
            return None
                    
    
    def get_hexagon_at_click(self, point):
        for i in range(11):
            for j in range(11):
                hexagon = self.board[i][j]
                if hexagon is not None and hexagon.contains(point):
                    return i, j
        return None, None
    
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
                        pygame.draw.line(surface, (0, 0, 0), (x, y), (nx, ny), 16)

        for i in range(11):
            for j in range(11):
                if self.board[i][j] != None:
                    x, y = self.board[i][j].center
                    neighbours = self.get_neighbours(i, j)
                    for neighbour in neighbours:
                        nx, ny = self.board[neighbour[0]][neighbour[1]].center
                        pygame.draw.line(surface, (255, 255, 255), (x, y), (nx, ny), 8)

        return surface

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
                    i, j = self.board.get_hexagon_at_click(mouse_pos)
                    print(f"Clicked hexagon coordinates: i={i}, j={j}")

            self.clock.tick(self.fps)

            self.play_video(self.screen)
            surface_board = self.board.draw()
            self.screen.blit(surface_board, (0, 0))
            # surface_hexagons = self.board.draw_hexagons()
            # self.screen.blit(surface_hexagons, (0, 0))

            pygame.display.flip()

if __name__ == "__main__":
    Game(screen).run()