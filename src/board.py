import pygame

from math import sqrt

from src.hexagon import Hexagon

class Board:
    def __init__(self) -> None:
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
        pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)

        # Load images for rings
        self.ring_img_p1 = pygame.image.load("assets/graphics/rings/RING_P1.png")
        self.ring_img_p2 = pygame.image.load("assets/graphics/rings/RING_P2.png")
        self.ring_img_p1 = self.ring_img_p1.convert_alpha()
        self.ring_img_p2 = self.ring_img_p2.convert_alpha()
        self.ring_img_p1 = pygame.transform.scale(self.ring_img_p1, (65, 65))
        self.ring_img_p2 = pygame.transform.scale(self.ring_img_p2, (65, 65))
        self.ring_rect_p1 = self.ring_img_p1.get_rect(center=(0, 0))
        self.ring_rect_p2 = self.ring_img_p2.get_rect(center=(0, 0))

        # Load images for markers
        self.marker_img_p1 = pygame.image.load("assets/graphics/markers/MARKER_P1.png")
        self.marker_img_p2 = pygame.image.load("assets/graphics/markers/MARKER_P2.png")
        self.marker_img_p1 = self.marker_img_p1.convert_alpha()
        self.marker_img_p2 = self.marker_img_p2.convert_alpha()
        self.marker_img_p1 = pygame.transform.scale(self.marker_img_p1, (65, 65))
        self.marker_img_p2 = pygame.transform.scale(self.marker_img_p2, (65, 65))
        self.marker_rect_p1 = self.marker_img_p1.get_rect(center=(0, 0))
        self.marker_rect_p2 = self.marker_img_p2.get_rect(center=(0, 0))

    def init_board(self) -> None:
        """
        Initialize the board with Hexagons.
        """
        size = 48
        horiz = 3/2*size
        vert = sqrt(3)*size/2

        startx, starty = 2*size, size/2
        x, y = startx, starty

        for i in range(11):
            for j in range(11):
                if self.board[i][j] == 1:
                    self.board[i][j] = Hexagon(x, y, size)
                x += horiz
                y += vert
            x = startx
            y = starty + vert * 2
            starty = y

    def board_state(self) -> list[list[str]]:
        """
        Get the state of the board.
        :return: list[list[str]], State of the board.
        """
        return [[(hexagon.state, hexagon.marker) if hexagon is not None else None for hexagon in row] for row in self.board]
    
    def update_board(self, state: list[list[str]]) -> None:
        """
        Update the board with the given state.
        :param state: list[list[str]], State of the board.
        """
        for i in range(11):
            for j in range(11):
                if state[i][j] is not None:
                    self.board[i][j].state = state[i][j][0]
                    self.board[i][j].marker = state[i][j][1]

    def get_neighbours(self, i: int, j: int) -> list[tuple[int, int]]:
        """
        Get the coordinates of the neighbors of a hexagon on the board. Used to draw the board lines.
        :param i: int, Row index of the hexagon.
        :param j: int, Column index of the hexagon.
        :return: list[tuple(int, int)], List of coordinates of neighboring hexagons.
        """
        vector = [
            (-1, 0),
            (-1, 1),
            (0, 1), 
            (1, 0),
            (1, -1),
            (0, -1) 
        ]

        return [(i+y, j+x) for y, x in vector if 0 <= i+y < 11 and 0 <= j+x < 11 and self.board[i+y][j+x] is not None]
    
    def get_lines(self, i: int, j: int) -> list[list[tuple[int, int]]]:
        """
        Get the lines passing through a given hexagon on the board.
        :param i: int, Row index of the hexagon.
        :param j: int, Column index of the hexagon.
        :return: list[list[tuple(int, int)]], List of lines passing through the hexagon.
        """
        vertical_up = self.get_cells_between(0, j, i, j)
        vertical_up = vertical_up[::-1]
        vertical_down = self.get_cells_between(i, j, 10, j)

        left_lower_diagonal = self.get_cells_between(i, 0, i, j)
        left_lower_diagonal = left_lower_diagonal[::-1]
        right_lower_diagonal = self.get_cells_between(i, j, i, 10)

        left_uper_diagonal = [(i, j)]
        right_uper_diagonal = [(i, j)]
        k, l = i, j
        while k < 10 and l > 0:
            k += 1
            l -= 1
            if self.board[k][l] is not None:
                left_uper_diagonal += [(k, l)]
        k, l = i, j
        while k > 0 and l < 10:
            k -= 1
            l += 1
            if self.board[k][l] is not None:
                right_uper_diagonal += [(k, l)]

        return [vertical_up, vertical_down, left_lower_diagonal, right_lower_diagonal, left_uper_diagonal, right_uper_diagonal]

    def get_cells_between(self, i: int, j: int, k:int, l:int) -> list[tuple[int, int]]:
        """
        Get the cells between two given coordinates (included) on the board.
        :param i: int, Row index of the first cell.
        :param j: int, Column index of the first cell.
        :param k: int, Row index of the second cell.
        :param l: int, Column index of the second cell.
        :return: list[tuple(int, int)], List of coordinates of cells between the given coordinates, which are included.
        """
        if j==l:
            return [(y, j) for y in range(min(i, k), max(i, k)+1) if self.board[y][j] is not None]
        elif i==k:
            return [(i, x) for x in range(min(j, l), max(j, l)+1) if self.board[i][x] is not None]
        elif abs(i-k) == abs(j-l):
            return [(y, x) for y, x in zip(range(max(i, k), min(i, k)-1, -1), range(min(j, l), max(j, l)+1)) if self.board[y][x] is not None]
        else:
            return None
    
    def valid_moves(self, i: int, j: int) -> list[tuple[int, int]]:
        """
        Get valid moves for a player from a specific hexagon.
        :param i: int, Row index of the hexagon
        :param j: int, Column index of the hexagon
        :return: list[tuple(int, int)], List of valid moves (coordinates) for the player.
        """
        possible_cells = []
        lines = self.get_lines(i, j)

        for line in lines:
            if line is None:
                continue
            for k in range(1, len(line)):
                coord_i, coord_j = line[k][0], line[k][1]
                if self.board[coord_i][coord_j].state == "EMPTY" and self.board[coord_i][coord_j].marker == "EMPTY":
                    possible_cells.append((coord_i, coord_j))
                    if k-1 > 0 and self.board[line[k-1][0]][line[k-1][1]].marker.startswith("MARKER"):
                        break
                elif self.board[coord_i][coord_j].state.startswith("RING"):
                    break
        return possible_cells
    
    def flip_markers(self, i: int, j: int, k: int, l: int) -> None:
        """
        Flip markers between two hexagons on the board.
        :param i: int, Row index of the first hexagon.
        :param j: int, Column index of the first hexagon.
        :param k: int, Row index of the second hexagon.
        :param l: int, Column index of the second hexagon.
        """
        cells = self.get_cells_between(i, j, k, l)
        cells.pop(0)
        cells.pop(-1)
        for cell in cells:
            i, j = cell
            self.board[i][j].marker = "MARKER_P2" if self.board[i][j].marker == "MARKER_P1" else "MARKER_P1" if self.board[i][j].marker == "MARKER_P2" else "EMPTY"
    
    def lines_to_check(self) -> list[list[tuple[int, int]]]:
        """
        Get the lines to check for a win condition.
        :return: list[list[tuple(int, int)]], List of lines to check for a win condition.
        """
        lines = []

        for i in range(11):
            for j in range(7):
                lines.append([(i, j), (i, j+1), (i, j+2), (i, j+3), (i, j+4)])
        
        for i in range(7):
            for j in range(11):
                lines.append([(i, j), (i+1, j), (i+2, j), (i+3, j), (i+4, j)])

        diagonal_start = [(6, 0), (7, 0), (8, 0), (9, 0), (9, 1), (10, 1), (10, 2), (10, 3), (10, 4)]
        for i, j in diagonal_start:
            while i-4 >= 0 and j+4 < 11:
                lines.append([(i, j), (i-1, j+1), (i-2, j+2), (i-3, j+3), (i-4, j+4)])
                i -= 1
                j += 1

        return lines

    def check_line_win(self, line: list[tuple[int, int]], marker) -> bool:
        """
        Check if a line contains 5 markers of the same player.
        :param line: list[tuple(int, int)], List of coordinates of the line to check.
        :return: bool, True if the line contains 5 markers of the same player, False otherwise.
        """
        markers = [self.board[i][j].marker for i, j in line if self.board[i][j] is not None]
        return len(markers) == 5 and markers.count(marker) == 5

    def check_win(self, player) -> str:
        """
        Check if a player has won the game.
        :return: str, Name of the player who has won the game, or None if no player has won yet.
        """
        player = "MARKER_P" + player[-1]
        lines = self.lines_to_check()
        aligned_lines = []

        for line in lines:
            if self.check_line_win(line, player):
                aligned_lines.append(line)
        return None if len(aligned_lines) == 0 else aligned_lines

    def get_hexagon(self, point: tuple[float, float]) -> tuple[int, int]:
        """
        Get the coordinates of the hexagon clicked on the board.
        :param point: tuple(float, float), Coordinates (x, y) of the clicked point.
        :return: tuple(int, int), Row and column indices of the clicked hexagon.
        """
        for i in range(11):
            for j in range(11):
                hexagon = self.board[i][j]
                if hexagon is not None and hexagon.contains(point):
                    return i, j
        return None, None

    def draw_board(self) -> pygame.Surface:
        """
        Draw lines between neighboring hexagons on the board surface.
        :return: pygame.Surface, Surface with lines drawn between neighboring hexagons (draws the empty board).
        """
        surface = pygame.Surface((1080, 1080), pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()

        # Draw background black thicker lines
        for i in range(11):
            for j in range(11):
                if self.board[i][j] is not None:
                    x, y = self.board[i][j].center
                    neighbours = self.get_neighbours(i, j)
                    for neighbour in neighbours:
                        nx, ny = self.board[neighbour[0]][neighbour[1]].center
                        pygame.draw.line(surface, (0, 0, 0), (x, y), (nx, ny), 16)
        
        # Draw white thinner lines on top of the black lines
        for i in range(11):
            for j in range(11):
                if self.board[i][j] != None:
                    x, y = self.board[i][j].center
                    neighbours = self.get_neighbours(i, j)
                    for neighbour in neighbours:
                        nx, ny = self.board[neighbour[0]][neighbour[1]].center
                        pygame.draw.line(surface, (255, 255, 255), (x, y), (nx, ny), 8)

        return surface
    
    def draw_player_elements(self, surface: pygame.Surface) -> pygame.Surface:
        """
        Draw player elements (rings and markers) on the board surface.
        :param surface: pygame.Surface, Surface on which to draw player elements.
        :return: pygame.Surface, Surface with player elements drawn.
        """
        for i in range(11):
            for j in range(11):
                if self.board[i][j] != None:
                    x, y = self.board[i][j].center

                    if self.board[i][j].state == "RING_P1":
                        surface.blit(self.ring_img_p1, self.ring_rect_p1.move(x, y))

                    elif self.board[i][j].state == "RING_P2":
                        surface.blit(self.ring_img_p2, self.ring_rect_p2.move(x, y))
                    
                    if self.board[i][j].marker == "MARKER_P1":
                        surface.blit(self.marker_img_p1, self.marker_rect_p1.move(x, y))

                    elif self.board[i][j].marker == "MARKER_P2":
                        surface.blit(self.marker_img_p2, self.marker_rect_p2.move(x, y))
        return surface