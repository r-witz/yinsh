import pygame # type: ignore
from sys import exit
from math import sqrt
import cv2 # type: ignore



# Screen should be passed as argument from menu to Game()
pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN|pygame.SCALED)
pygame.display.set_caption("YINSH")

class Hexagone:
    def __init__(self, x, y, size, q, r):
        self.state = "EMPTY" # EMPTY, RING_P1, RING_P2
        self.marker = "EMPTY" # EMPTY, MARKER_P1, MARKER_P2

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
                if self.board[i][j] is not None:
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
    
    def draw_player_elements(self, surface):
        for i in range(11):
            for j in range(11):
                if self.board[i][j] != None:
                    x, y = self.board[i][j].center

                    if self.board[i][j].state == "RING_P1":
                        pygame.draw.circle(surface, (0, 0, 255), (x, y), 26)  # Blue ring

                    elif self.board[i][j].state == "RING_P2":
                        pygame.draw.circle(surface, (255, 0, 0), (x, y), 26)  # Red ring
                    
                    if self.board[i][j].marker == "MARKER_P1":
                        pygame.draw.circle(surface, (0, 0, 0), (x, y), 16)
                        pygame.draw.circle(surface, (0, 0, 255), (x, y), 12)  # Blue marker

                    elif self.board[i][j].marker == "MARKER_P2":
                        pygame.draw.circle(surface, (0, 0, 0), (x, y), 16)
                        pygame.draw.circle(surface, (255, 0, 0), (x, y), 12)  # Red marker
        return surface

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.rings = []

    def place_ring(self, hexagon):
        if hexagon.state == "EMPTY":
            hexagon.state = "RING_P" + self.name[-1]  # Assuming player's name is "PlayerX"
            self.rings.append(hexagon)
            return hexagon
        else:
            return False

    def place_marker(self, hexagon):
        if hexagon.state == "RING_P" + self.name[-1]:
            hexagon.marker = "MARKER_P" + self.name[-1]  # Assuming player's name is "PlayerX"
            return hexagon
        else:
            return False

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.board = Board()

        self.video = cv2.VideoCapture("assets/graphics/background/menu.mp4")
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

        self.p1 = Player("Player1", "blue")
        self.p2 = Player("Player2", "red")
        self.player_to_play = self.p1

    def play_video(self, surface):
        success, video_image = self.video.read()
        if not success:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, video_image = self.video.read()
        video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
        surface.blit(video_surf, (0, 0))

    def run(self, screen):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # handle all game logic on click (LMAO c'est du caca mais ça marche) 
                    # TODO Clean in functions to handle this
                    mouse_pos = pygame.mouse.get_pos()
                    i, j = self.board.get_hexagon_at_click(mouse_pos)
                    if i is None or j is None:
                        continue
                    selected_hexagon = self.board.board[i][j]
                    if len(self.p1.rings) == 5 and len(self.p2.rings) == 5:
                        move_function = self.player_to_play.place_marker
                    else:
                        move_function = self.player_to_play.place_ring
                    move = move_function(selected_hexagon)
                    if move:
                        self.board.board[i][j] == move
                        self.player_to_play = self.p1 if self.player_to_play == self.p2 else self.p2


            self.clock.tick(self.fps)

            self.play_video(screen)
            surface_board = self.board.draw()
            surface_board = self.board.draw_player_elements(surface_board)
            screen.blit(surface_board, (0, 0))

            # Draw hitboxes for debug purposes
            # surface_hexagons = self.board.draw_hexagons()
            # screen.blit(surface_hexagons, (0, 0))

            pygame.display.flip()

if __name__ == "__main__":
    Game().run(screen)